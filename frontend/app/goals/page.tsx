"use client";

import { FormEvent, useCallback, useEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";
import {
  GoalFundingSummary,
  formatThb,
  inputClass,
  messageFor,
  priorityLabel,
  typeLabel,
  type AllocationsState,
} from "@/components/goals/GoalPlanningSections";
import {
  buildSourceFundingOverview,
  sourceKey,
  type FundingSourceKey,
  type SourceFundingOverviewRow,
} from "@/lib/goalFunding";
import { computePortfolioCurrentValue } from "@/lib/wealthOverview";
import { usePortfolio } from "@/lib/PortfolioContext";
import {
  createWealthGoal,
  getHoldings,
  getPortfolioPrices,
  listCashAccounts,
  listGoalFundingAllocations,
  listWealthGoals,
  updateWealthGoal,
  type CashAccount,
  type GoalFundingAllocation,
  type GoalFundingSourceKind,
  type WealthGoal,
  type WealthGoalPriority,
  type WealthGoalType,
} from "@/lib/api";

type CashAccountsState = CashAccount[] | { error: string } | undefined;

const GOAL_TYPES: WealthGoalType[] = [
  "RETIREMENT",
  "HOUSE",
  "WEDDING",
  "EDUCATION",
  "VACATION",
  "EMERGENCY_FUND",
  "FIRE",
  "OTHER",
];

const PRIORITIES: WealthGoalPriority[] = ["HIGH", "MEDIUM", "LOW"];

export default function GoalsPage() {
  const [goals, setGoals] = useState<WealthGoal[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [mutationError, setMutationError] = useState("");
  const [showArchived, setShowArchived] = useState(false);
  const [allocationsByGoal, setAllocationsByGoal] = useState<Record<number, AllocationsState>>({});
  const [cashAccountsState, setCashAccountsState] = useState<CashAccountsState>(undefined);
  const [portfolioValueById, setPortfolioValueById] = useState<Record<number, number | "error">>({});

  const { portfolios: portfolioCatalog, loading: portfoliosLoading, error: portfoliosError } = usePortfolio();

  const refreshGenerationRef = useRef(0);
  // Portfolio ids whose holdings+prices have already been requested for the
  // CURRENT refresh generation. Kept in a ref, not state, so that a settling
  // valuation cannot re-run the fan-out effect and re-issue requests that are
  // still in flight — getPortfolioPrices can trigger live provider work.
  const requestedPortfolioIdsRef = useRef<Set<number>>(new Set());
  const mountedRef = useRef(true);
  useEffect(() => {
    mountedRef.current = true;
    return () => {
      mountedRef.current = false;
    };
  }, []);

  const [name, setName] = useState("");
  const [goalType, setGoalType] = useState<WealthGoalType>("OTHER");
  const [targetAmount, setTargetAmount] = useState("");
  const [targetDate, setTargetDate] = useState("");
  const [priority, setPriority] = useState<WealthGoalPriority>("MEDIUM");
  const [note, setNote] = useState("");

  const [editing, setEditing] = useState<WealthGoal | null>(null);
  const [editName, setEditName] = useState("");
  const [editType, setEditType] = useState<WealthGoalType>("OTHER");
  const [editTargetAmount, setEditTargetAmount] = useState("");
  const [editTargetDate, setEditTargetDate] = useState("");
  const [editPriority, setEditPriority] = useState<WealthGoalPriority>("MEDIUM");
  const [editNote, setEditNote] = useState("");

  // One coherent, generation-guarded refresh: fetches the full goal list
  // (active + archived — the "Show archived" toggle is presentation-only and
  // never triggers a fetch), then each goal's allocations exactly once,
  // reused for both per-goal funding cards and the workspace-wide Funding
  // source health rollup below. Stale responses (superseded refresh, or a
  // response arriving after unmount) are dropped rather than applied.
  const refresh = useCallback(async () => {
    const generation = ++refreshGenerationRef.current;
    const isCurrent = () => mountedRef.current && refreshGenerationRef.current === generation;
    requestedPortfolioIdsRef.current = new Set();

    setLoading(true);
    setError("");
    setAllocationsByGoal({});
    setCashAccountsState(undefined);
    setPortfolioValueById({});

    let loadedGoals: WealthGoal[];
    try {
      loadedGoals = await listWealthGoals(true);
    } catch (err) {
      if (!isCurrent()) return;
      setGoals([]);
      setError(messageFor(err, "Unable to load goals."));
      setLoading(false);
      return;
    }
    if (!isCurrent()) return;
    setGoals(loadedGoals);
    setLoading(false);

    void listCashAccounts(true)
      .then((accounts) => {
        if (isCurrent()) setCashAccountsState(accounts);
      })
      .catch((err) => {
        if (isCurrent()) setCashAccountsState({ error: messageFor(err, "Unable to load cash accounts.") });
      });

    const entries = await Promise.all(
      loadedGoals.map(async (item) => {
        try {
          return [item.id, await listGoalFundingAllocations(item.id)] as const;
        } catch (err) {
          return [item.id, { error: messageFor(err, "Unable to load funding progress.") }] as const;
        }
      })
    );
    if (!isCurrent()) return;
    const nextAllocationsByGoal: Record<number, AllocationsState> = {};
    for (const [id, result] of entries) nextAllocationsByGoal[id] = result;
    setAllocationsByGoal(nextAllocationsByGoal);
  }, []);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  const active = goals.filter((item) => !item.is_archived);
  const archived = goals.filter((item) => item.is_archived);

  // Complete only when every goal's allocation fetch succeeded — a partial
  // set would under-report a shared source's true total designation, so an
  // incomplete set is never used to build the workspace rollup below.
  const allocationEvidenceComplete = !error && goals.every((item) => Array.isArray(allocationsByGoal[item.id]));
  const allocationFetchesPending = !error && goals.some((item) => allocationsByGoal[item.id] === undefined);

  const allWorkspaceAllocations = useMemo<GoalFundingAllocation[]>(() => {
    if (!allocationEvidenceComplete) return [];
    const combined: GoalFundingAllocation[] = [];
    for (const item of goals) {
      const result = allocationsByGoal[item.id];
      if (Array.isArray(result)) combined.push(...result);
    }
    return combined;
  }, [allocationEvidenceComplete, goals, allocationsByGoal]);

  const referencedPortfolioIds = useMemo(() => {
    const ids = new Set<number>();
    for (const allocation of allWorkspaceAllocations) {
      if (allocation.portfolio_id != null) ids.add(allocation.portfolio_id);
    }
    return ids;
  }, [allWorkspaceAllocations]);

  // Only after allocation evidence is complete, and only once per referenced
  // portfolio, fetch that portfolio's holdings + prices and reduce them
  // through the canonical computePortfolioCurrentValue (frontend/lib/wealthOverview.ts)
  // — not a second valuation formula. A portfolio catalog failure or an id
  // absent from PortfolioContext's list leaves that source unresolved, which
  // renders as UNAVAILABLE rather than a fabricated value.
  useEffect(() => {
    if (!allocationEvidenceComplete || portfoliosLoading || portfoliosError) return;
    const generation = refreshGenerationRef.current;
    for (const portfolioId of referencedPortfolioIds) {
      if (requestedPortfolioIdsRef.current.has(portfolioId)) continue;
      const portfolio = portfolioCatalog.find((item) => item.id === portfolioId);
      // Not in the catalog yet: leave it unrequested so a later catalog update
      // can still resolve it; until then it renders as UNAVAILABLE.
      if (!portfolio) continue;
      requestedPortfolioIdsRef.current.add(portfolioId);
      void (async () => {
        try {
          const [items, prices] = await Promise.all([getHoldings(portfolioId), getPortfolioPrices(portfolioId)]);
          if (!mountedRef.current || refreshGenerationRef.current !== generation) return;
          const { value } = computePortfolioCurrentValue(portfolio, items, prices);
          setPortfolioValueById((prev) => ({ ...prev, [portfolioId]: value }));
        } catch {
          if (!mountedRef.current || refreshGenerationRef.current !== generation) return;
          setPortfolioValueById((prev) => ({ ...prev, [portfolioId]: "error" }));
        }
      })();
    }
  }, [allocationEvidenceComplete, referencedPortfolioIds, portfolioCatalog, portfoliosLoading, portfoliosError]);

  const currentValueBySource = useMemo(() => {
    const map = new Map<FundingSourceKey, number | null>();
    for (const allocation of allWorkspaceAllocations) {
      const kind: GoalFundingSourceKind = allocation.cash_account_id != null ? "CASH_ACCOUNT" : "PORTFOLIO";
      const id = (allocation.cash_account_id ?? allocation.portfolio_id) as number;
      const key = sourceKey(kind, id);
      if (map.has(key)) continue;
      if (kind === "CASH_ACCOUNT") {
        const value = Array.isArray(cashAccountsState)
          ? cashAccountsState.find((account) => account.id === id)?.balance ?? null
          : null;
        map.set(key, value);
      } else {
        const value = portfolioValueById[id];
        map.set(key, typeof value === "number" ? value : null);
      }
    }
    return map;
  }, [allWorkspaceAllocations, cashAccountsState, portfolioValueById]);

  const overviewRows: SourceFundingOverviewRow[] = useMemo(
    () => buildSourceFundingOverview(allWorkspaceAllocations, currentValueBySource),
    [allWorkspaceAllocations, currentValueBySource]
  );

  async function handleCreate(event: FormEvent) {
    event.preventDefault();
    setMutationError("");
    const parsed = Number(targetAmount);
    if (!name.trim() || !targetAmount.trim() || !Number.isFinite(parsed) || parsed <= 0) {
      setMutationError("Enter a goal name and a positive target amount.");
      return;
    }
    try {
      await createWealthGoal({
        name: name.trim(),
        goal_type: goalType,
        target_amount: parsed,
        currency: "THB",
        target_date: targetDate || null,
        priority,
        note: note.trim() || null,
      });
      setName("");
      setGoalType("OTHER");
      setTargetAmount("");
      setTargetDate("");
      setPriority("MEDIUM");
      setNote("");
      await refresh();
    } catch (err) {
      setMutationError(messageFor(err, "Unable to create goal."));
    }
  }

  function openEdit(item: WealthGoal) {
    setMutationError("");
    setEditing(item);
    setEditName(item.name);
    setEditType(item.goal_type);
    setEditTargetAmount(String(item.target_amount));
    setEditTargetDate(item.target_date ?? "");
    setEditPriority(item.priority);
    setEditNote(item.note ?? "");
  }

  async function handleEdit(event: FormEvent) {
    event.preventDefault();
    if (!editing) return;
    setMutationError("");
    const parsed = Number(editTargetAmount);
    if (!editName.trim() || !editTargetAmount.trim() || !Number.isFinite(parsed) || parsed <= 0) {
      setMutationError("Enter a goal name and a positive target amount.");
      return;
    }
    try {
      await updateWealthGoal(editing.id, {
        name: editName.trim(),
        goal_type: editType,
        target_amount: parsed,
        target_date: editTargetDate || null,
        priority: editPriority,
        note: editNote.trim() || null,
      });
      setEditing(null);
      await refresh();
    } catch (err) {
      setMutationError(messageFor(err, "Unable to update goal."));
    }
  }

  async function setArchived(item: WealthGoal, isArchived: boolean) {
    setMutationError("");
    try {
      await updateWealthGoal(item.id, { is_archived: isArchived });
      await refresh();
    } catch (err) {
      setMutationError(messageFor(err, isArchived ? "Unable to archive goal." : "Unable to restore goal."));
    }
  }

  // Presentation-only: the full goal list (active + archived) is already
  // loaded by refresh(); toggling never causes a network request.
  function toggleArchived() {
    setShowArchived((prev) => !prev);
  }

  return (
    <div className="space-y-6 max-w-3xl">
      <div>
        <h1 className="text-2xl font-bold">Goals</h1>
        <p className="text-sm text-gray-500 mt-1">
          Manage whole-life financial goals — retirement, a house, a wedding, and more. Open a goal to review its funding and deterministic planning tools.
        </p>
      </div>

      <form onSubmit={handleCreate} className="bg-white border rounded-xl p-4 space-y-3 shadow-sm">
        <h2 className="font-semibold">Add goal</h2>
        <div className="grid gap-3 sm:grid-cols-2">
          <Field label="Name"><input aria-label="Goal name" value={name} onChange={(event) => setName(event.target.value)} className={inputClass} /></Field>
          <Field label="Type"><TypeSelect ariaLabel="Goal type" value={goalType} onChange={setGoalType} /></Field>
          <Field label="Target amount"><input aria-label="Target amount" type="number" step="0.01" value={targetAmount} onChange={(event) => setTargetAmount(event.target.value)} className={inputClass} /></Field>
          <Field label="Target date (optional)"><input aria-label="Target date" type="date" value={targetDate} onChange={(event) => setTargetDate(event.target.value)} className={inputClass} /></Field>
          <Field label="Priority"><PrioritySelect ariaLabel="Goal priority" value={priority} onChange={setPriority} /></Field>
          <Field label="Note (optional)"><input aria-label="Note" value={note} onChange={(event) => setNote(event.target.value)} className={inputClass} /></Field>
        </div>
        <p className="text-xs text-gray-500">Currency: <strong>THB</strong> (fixed for Wealth Goals Foundation v1)</p>
        <PrimaryButton>Add goal</PrimaryButton>
      </form>

      {mutationError && <p role="alert" className="text-sm text-red-600">{mutationError}</p>}

      {editing && (
        <form onSubmit={handleEdit} className="bg-blue-50 border border-blue-200 rounded-xl p-4 space-y-3">
          <h2 className="font-semibold">Edit {editing.name}</h2>
          <div className="grid gap-3 sm:grid-cols-2">
            <Field label="Name"><input aria-label="Edit goal name" value={editName} onChange={(event) => setEditName(event.target.value)} className={inputClass} /></Field>
            <Field label="Type"><TypeSelect ariaLabel="Edit goal type" value={editType} onChange={setEditType} /></Field>
            <Field label="Target amount"><input aria-label="Edit target amount" type="number" step="0.01" value={editTargetAmount} onChange={(event) => setEditTargetAmount(event.target.value)} className={inputClass} /></Field>
            <Field label="Target date"><input aria-label="Edit target date" type="date" value={editTargetDate} onChange={(event) => setEditTargetDate(event.target.value)} className={inputClass} /></Field>
            <Field label="Priority"><PrioritySelect ariaLabel="Edit goal priority" value={editPriority} onChange={setEditPriority} /></Field>
            <Field label="Note"><input aria-label="Edit note" value={editNote} onChange={(event) => setEditNote(event.target.value)} className={inputClass} /></Field>
          </div>
          <Actions><PrimaryButton>Save changes</PrimaryButton><Cancel onClick={() => setEditing(null)} /></Actions>
        </form>
      )}

      <section className="space-y-3">
        <div className="flex items-center justify-between gap-3 flex-wrap">
          <h2 className="text-lg font-semibold">Active goals</h2>
          <button type="button" onClick={() => void toggleArchived()} className="text-sm text-blue-600 hover:underline">{showArchived ? "Hide archived" : "Show archived"}</button>
        </div>
        {loading ? (
          <p className="text-sm text-gray-400">Loading goals…</p>
        ) : error ? (
          <div className="text-sm text-red-600 space-y-2"><p role="alert">{error}</p><button type="button" onClick={() => void refresh()} className="text-blue-600 hover:underline">Try again</button></div>
        ) : active.length === 0 ? (
          <p className="text-sm text-gray-500">No active goals yet. Add your first goal above.</p>
        ) : (
          <div className="space-y-3">{active.map((item) => (
            <GoalCard key={item.id} item={item} allocations={allocationsByGoal[item.id]} onEdit={openEdit} onArchive={() => void setArchived(item, true)} />
          ))}</div>
        )}
      </section>

      <section className="space-y-3 pt-2 border-t" aria-labelledby="funding-source-health-heading">
        <h2 id="funding-source-health-heading" className="text-lg font-semibold">Funding source health</h2>
        {loading || allocationFetchesPending ? (
          <p className="text-sm text-gray-400">Loading funding source health…</p>
        ) : error || !allocationEvidenceComplete ? (
          <p role="alert" className="text-sm text-red-600">
            Funding source health is unavailable — allocation evidence is incomplete.
          </p>
        ) : goals.length === 0 ? (
          <p className="text-sm text-gray-500">No funding sources to show yet.</p>
        ) : overviewRows.length === 0 ? (
          <p className="text-sm text-gray-500">No funding sources designated yet.</p>
        ) : (
          <ul className="space-y-1.5 bg-white border rounded-xl p-4 shadow-sm">
            {overviewRows.map((row) => (
              <SourceHealthRow key={row.key} row={row} />
            ))}
          </ul>
        )}
      </section>

      {showArchived && !loading && !error && (
        <section className="space-y-3 pt-2 border-t">
          <h2 className="text-lg font-semibold text-gray-600">Archived goals</h2>
          {archived.length === 0 ? <p className="text-sm text-gray-500">No archived goals.</p> : archived.map((item) => (
            <div key={item.id} className="bg-gray-50 border rounded-xl p-4 flex items-center justify-between gap-4">
              <div>
                <p className="font-medium text-gray-600">{item.name}</p>
                <p className="text-sm text-gray-500">{typeLabel(item.goal_type)} · {priorityLabel(item.priority)} priority</p>
                <p className="text-sm text-gray-600">{formatThb(item.target_amount)} target{item.target_date ? ` · by ${item.target_date}` : ""}</p>
              </div>
              <button type="button" onClick={() => void setArchived(item, false)} className="text-sm text-blue-600 hover:underline">Restore</button>
            </div>
          ))}
        </section>
      )}
    </div>
  );
}

function GoalCard({
  item,
  allocations,
  onEdit,
  onArchive,
}: {
  item: WealthGoal;
  allocations: AllocationsState;
  onEdit: (item: WealthGoal) => void;
  onArchive: () => void;
}) {
  return (
    <article className="bg-white border rounded-xl p-4 shadow-sm space-y-3">
      <div className="flex items-start justify-between gap-4 flex-wrap">
        <div>
          <p className="font-semibold">{item.name}</p>
          <p className="text-sm text-gray-500">{typeLabel(item.goal_type)} · {priorityLabel(item.priority)} priority</p>
          <p className="text-sm text-gray-600 mt-1">{formatThb(item.target_amount)} target · {item.target_date ? `by ${item.target_date}` : "no target date"}</p>
        </div>
        <div className="flex gap-3 text-sm flex-wrap">
          <Link href={`/goals/${item.id}`} className="text-blue-600 hover:underline">View plan →</Link>
          <button type="button" onClick={() => onEdit(item)} className="text-blue-600 hover:underline">Edit</button>
          <button type="button" onClick={onArchive} className="text-red-600 hover:underline">Archive</button>
        </div>
      </div>
      <GoalFundingSummary allocations={allocations} targetAmount={item.target_amount} compact />
    </article>
  );
}

function SourceHealthRow({ row }: { row: SourceFundingOverviewRow }) {
  return (
    <li className="text-sm border-b last:border-0 pb-1.5">
      <div className="flex items-center justify-between gap-2 flex-wrap">
        <span className="text-gray-700">
          {row.sourceName}{" "}
          <span className="text-xs text-gray-400 ml-1">
            ({row.sourceKind === "CASH_ACCOUNT" ? "Cash Account" : "Portfolio"}
            {row.sourceIsArchived ? ", archived" : ""})
          </span>
        </span>
        <span className="font-medium">{formatThb(row.health.totalDesignated)} designated</span>
      </div>
      {row.health.status === "UNAVAILABLE" ? (
        <p className="text-xs text-gray-400 mt-0.5">Current value unavailable · Funding health unavailable</p>
      ) : row.health.status === "OVER_ALLOCATED" ? (
        <p className="text-xs text-amber-600 mt-0.5">
          Current value {formatThb(row.health.currentValue as number)} · Over-allocated by {formatThb(row.health.shortfall as number)}
        </p>
      ) : (
        <p className="text-xs text-gray-500 mt-0.5">Current value {formatThb(row.health.currentValue as number)} · Funding health: Supported</p>
      )}
    </li>
  );
}

function TypeSelect({ ariaLabel, value, onChange }: { ariaLabel: string; value: WealthGoalType; onChange: (value: WealthGoalType) => void }) {
  return <select aria-label={ariaLabel} value={value} onChange={(event) => onChange(event.target.value as WealthGoalType)} className={inputClass}>{GOAL_TYPES.map((item) => <option key={item} value={item}>{typeLabel(item)}</option>)}</select>;
}

function PrioritySelect({ ariaLabel, value, onChange }: { ariaLabel: string; value: WealthGoalPriority; onChange: (value: WealthGoalPriority) => void }) {
  return <select aria-label={ariaLabel} value={value} onChange={(event) => onChange(event.target.value as WealthGoalPriority)} className={inputClass}>{PRIORITIES.map((item) => <option key={item} value={item}>{priorityLabel(item)}</option>)}</select>;
}

function Field({ label, children }: { label: string; children: React.ReactNode }) { return <label className="text-sm">{label}{children}</label>; }
function PrimaryButton({ children }: { children: React.ReactNode }) { return <button type="submit" className="bg-blue-600 text-white px-3 py-1.5 rounded text-sm hover:bg-blue-700">{children}</button>; }
function Cancel({ onClick }: { onClick: () => void }) { return <button type="button" onClick={onClick} className="text-sm text-gray-600">Cancel</button>; }
function Actions({ children }: { children: React.ReactNode }) { return <div className="flex gap-2 mt-3">{children}</div>; }
