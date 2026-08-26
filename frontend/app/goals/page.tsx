"use client";

import { FormEvent, useEffect, useMemo, useState } from "react";
import {
  aggregateDesignatedBySource,
  computeGoalFunding,
  computeSourceFundingHealth,
  sourceKey,
  type SourceFundingHealth,
} from "@/lib/goalFunding";
import { computePortfolioCurrentValue } from "@/lib/wealthOverview";
import {
  createGoalFundingAllocation,
  createWealthGoal,
  deleteGoalFundingAllocation,
  getHoldings,
  getPortfolioPrices,
  listCashAccounts,
  listGoalFundingAllocations,
  listPortfolios,
  listWealthGoals,
  updateGoalFundingAllocation,
  updateWealthGoal,
  type CashAccount,
  type GoalFundingAllocation,
  type GoalFundingSourceKind,
  type Portfolio,
  type WealthGoal,
  type WealthGoalPriority,
  type WealthGoalType,
} from "@/lib/api";

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

const typeLabel = (value: WealthGoalType) => ({
  RETIREMENT: "Retirement",
  HOUSE: "House",
  WEDDING: "Wedding",
  EDUCATION: "Education",
  VACATION: "Vacation",
  EMERGENCY_FUND: "Emergency fund",
  FIRE: "FIRE",
  OTHER: "Other",
}[value]);

const priorityLabel = (value: WealthGoalPriority) => ({
  HIGH: "High",
  MEDIUM: "Medium",
  LOW: "Low",
}[value]);

const formatThb = (value: number) => value.toLocaleString("th-TH", {
  style: "currency",
  currency: "THB",
  minimumFractionDigits: 2,
});
const messageFor = (error: unknown, fallback: string) => error instanceof Error ? error.message : fallback;
const inputClass = "mt-1 block w-full border rounded px-3 py-2";

interface AllocationsLoadError {
  error: string;
}
type AllocationsState = GoalFundingAllocation[] | AllocationsLoadError | undefined;

export default function GoalsPage() {
  const [goals, setGoals] = useState<WealthGoal[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [mutationError, setMutationError] = useState("");
  const [showArchived, setShowArchived] = useState(false);

  // Funding sources reuse the existing Cash Account / Portfolio lists — no new
  // source-discovery endpoint. `cashAccounts` (active only) feeds the "add
  // source" dropdown per "active sources only for new allocations". `allCashAccounts`
  // (active + archived) is separately loaded so Funding Health can still look
  // up the current balance of a source an allocation references even after
  // that Cash Account is archived — archiving does not erase allocation evidence.
  const [cashAccounts, setCashAccounts] = useState<CashAccount[]>([]);
  const [allCashAccounts, setAllCashAccounts] = useState<CashAccount[]>([]);
  const [portfolios, setPortfolios] = useState<Portfolio[]>([]);

  useEffect(() => {
    void listCashAccounts(false).then(setCashAccounts).catch(() => {});
    void listCashAccounts(true).then(setAllCashAccounts).catch(() => {});
    void listPortfolios().then(setPortfolios).catch(() => {});
  }, []);

  // Goal Progress & Funding Health (Phase 6, Milestone 3) need every active
  // goal's allocations at once — a source's Funding Health is a total across
  // ALL goals that reference it, not just one. Lifted here (rather than each
  // goal card loading its own in isolation) so that cross-goal total can be
  // computed. `undefined` = not yet loaded, `"error"` = load failed (Goal
  // Progress must show "unavailable", never a fabricated 0%).
  const [allocationsByGoal, setAllocationsByGoal] = useState<Record<number, AllocationsState>>({});

  async function loadAllocations(goalId: number) {
    try {
      const result = await listGoalFundingAllocations(goalId);
      setAllocationsByGoal((prev) => ({ ...prev, [goalId]: result }));
    } catch (err) {
      setAllocationsByGoal((prev) => ({ ...prev, [goalId]: { error: messageFor(err, "Unable to load funding sources.") } }));
    }
  }

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

  async function load(includeArchived = showArchived) {
    setLoading(true);
    setError("");
    try {
      setGoals(await listWealthGoals(includeArchived));
    } catch (err) {
      setGoals([]);
      setError(messageFor(err, "Unable to load goals."));
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void load(false);
    // The initial request is intentionally active-only; the toggle controls the
    // include_archived query for subsequent requests.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const active = goals.filter((item) => !item.is_archived);
  const archived = goals.filter((item) => item.is_archived);
  const activeIdsKey = active.map((item) => item.id).join(",");

  useEffect(() => {
    for (const item of active) {
      if (allocationsByGoal[item.id] === undefined) void loadAllocations(item.id);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activeIdsKey]);

  // Portfolio current value has no stored column — it must be derived live,
  // the same way the rest of the app already derives it (cash_balance +
  // holdings * price). Fetched only for portfolios actually referenced by a
  // loaded allocation, not every portfolio in the workspace.
  const [portfolioValueById, setPortfolioValueById] = useState<Record<number, number | "error" | undefined>>({});

  const referencedPortfolioIds = useMemo(() => {
    const ids = new Set<number>();
    for (const result of Object.values(allocationsByGoal)) {
      if (!Array.isArray(result)) continue;
      for (const allocation of result) {
        if (allocation.portfolio_id != null) ids.add(allocation.portfolio_id);
      }
    }
    return ids;
  }, [allocationsByGoal]);

  useEffect(() => {
    let cancelled = false;
    for (const portfolioId of referencedPortfolioIds) {
      if (portfolioValueById[portfolioId] !== undefined) continue;
      const portfolio = portfolios.find((item) => item.id === portfolioId);
      if (!portfolio) continue; // portfolios list not loaded yet; effect re-runs once it is
      void (async () => {
        try {
          const [items, prices] = await Promise.all([getHoldings(portfolioId), getPortfolioPrices(portfolioId)]);
          if (cancelled) return;
          const { value } = computePortfolioCurrentValue(portfolio, items, prices);
          setPortfolioValueById((prev) => ({ ...prev, [portfolioId]: value }));
        } catch {
          if (cancelled) return;
          setPortfolioValueById((prev) => ({ ...prev, [portfolioId]: "error" }));
        }
      })();
    }
    return () => { cancelled = true; };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [referencedPortfolioIds, portfolios]);

  const designatedBySource = useMemo(() => {
    const loaded: GoalFundingAllocation[] = [];
    for (const result of Object.values(allocationsByGoal)) {
      if (Array.isArray(result)) loaded.push(...result);
    }
    return aggregateDesignatedBySource(loaded);
  }, [allocationsByGoal]);

  function fundingHealthForSource(kind: GoalFundingSourceKind, id: number): SourceFundingHealth {
    const totalDesignated = designatedBySource.get(sourceKey(kind, id)) ?? 0;
    const currentValue = kind === "CASH_ACCOUNT"
      ? allCashAccounts.find((account) => account.id === id)?.balance ?? null
      : (typeof portfolioValueById[id] === "number" ? (portfolioValueById[id] as number) : null);
    return computeSourceFundingHealth(totalDesignated, currentValue);
  }

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
      await load();
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
      await load();
    } catch (err) {
      setMutationError(messageFor(err, "Unable to update goal."));
    }
  }

  async function setArchived(item: WealthGoal, isArchived: boolean) {
    setMutationError("");
    try {
      await updateWealthGoal(item.id, { is_archived: isArchived });
      await load();
    } catch (err) {
      setMutationError(messageFor(err, isArchived ? "Unable to archive goal." : "Unable to restore goal."));
    }
  }

  async function toggleArchived() {
    const next = !showArchived;
    setShowArchived(next);
    await load(next);
  }

  return (
    <div className="space-y-6 max-w-3xl">
      <div>
        <h1 className="text-2xl font-bold">Goals</h1>
        <p className="text-sm text-gray-500 mt-1">
          Track whole-life financial goals — retirement, a house, a wedding, and more. Goal progress reflects only the
          funding you explicitly designate below; it is not linked to your current Net Worth.
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
        {loading ? <p className="text-sm text-gray-400">Loading goals…</p> : error ? <div className="text-sm text-red-600 space-y-2"><p role="alert">{error}</p><button type="button" onClick={() => void load()} className="text-blue-600 hover:underline">Try again</button></div> : active.length === 0 ? <p className="text-sm text-gray-500">No active goals yet. Add your first goal above.</p> : <div className="space-y-3">{active.map((item) => (
          <GoalCard
            key={item.id}
            item={item}
            cashAccounts={cashAccounts}
            portfolios={portfolios}
            allocations={allocationsByGoal[item.id]}
            onReloadAllocations={() => loadAllocations(item.id)}
            fundingHealthForSource={fundingHealthForSource}
            onEdit={openEdit}
            onArchive={() => void setArchived(item, true)}
          />
        ))}</div>}
      </section>

      {showArchived && !loading && !error && (
        <section className="space-y-3 pt-2 border-t">
          <h2 className="text-lg font-semibold text-gray-600">Archived goals</h2>
          {archived.length === 0 ? <p className="text-sm text-gray-500">No archived goals.</p> : archived.map((item) => <div key={item.id} className="bg-gray-50 border rounded-xl p-4 flex items-center justify-between gap-4"><div><p className="font-medium text-gray-600">{item.name}</p><p className="text-sm text-gray-500">{typeLabel(item.goal_type)} · {priorityLabel(item.priority)} priority</p><p className="text-sm text-gray-600">{formatThb(item.target_amount)} target{item.target_date ? ` · by ${item.target_date}` : ""}</p></div><button type="button" onClick={() => void setArchived(item, false)} className="text-sm text-blue-600 hover:underline">Restore</button></div>)}
        </section>
      )}
    </div>
  );
}

function GoalCard({
  item,
  cashAccounts,
  portfolios,
  allocations,
  onReloadAllocations,
  fundingHealthForSource,
  onEdit,
  onArchive,
}: {
  item: WealthGoal;
  cashAccounts: CashAccount[];
  portfolios: Portfolio[];
  allocations: AllocationsState;
  onReloadAllocations: () => Promise<void>;
  fundingHealthForSource: (kind: GoalFundingSourceKind, id: number) => SourceFundingHealth;
  onEdit: (item: WealthGoal) => void;
  onArchive: () => void;
}) {
  return (
    <div className="bg-white border rounded-xl p-4 shadow-sm space-y-3">
      <div className="flex items-start justify-between gap-4 flex-wrap">
        <div>
          <p className="font-semibold">{item.name}</p>
          <p className="text-sm text-gray-500">{typeLabel(item.goal_type)} · {priorityLabel(item.priority)} priority</p>
          <p className="text-lg font-medium mt-1">{formatThb(item.target_amount)} <span className="text-xs text-gray-500">target</span></p>
          <p className="text-xs text-gray-400 mt-1">{item.target_date ? `Target date: ${item.target_date}` : "No target date set"}</p>
          {item.note && <p className="text-sm text-gray-500 mt-1">{item.note}</p>}
        </div>
        <div className="flex gap-3 text-sm flex-wrap">
          <button type="button" onClick={() => onEdit(item)} className="text-blue-600 hover:underline">Edit</button>
          <button type="button" onClick={onArchive} className="text-red-600 hover:underline">Archive</button>
        </div>
      </div>
      <GoalFundingSummary allocations={allocations} targetAmount={item.target_amount} />
      <FundingSourcesSection
        goalId={item.id}
        cashAccounts={cashAccounts}
        portfolios={portfolios}
        allocations={allocations}
        onReload={onReloadAllocations}
        fundingHealthForSource={fundingHealthForSource}
      />
    </div>
  );
}

function GoalFundingSummary({ allocations, targetAmount }: { allocations: AllocationsState; targetAmount: number }) {
  if (allocations === undefined) {
    return <p className="text-xs text-gray-400 mt-2">Loading funding progress…</p>;
  }
  const funding = computeGoalFunding(targetAmount, Array.isArray(allocations) ? allocations : null);
  if (funding.designatedFunding === null) {
    return <p role="alert" className="text-xs text-red-600 mt-2">Goal progress unavailable — funding data failed to load.</p>;
  }
  return (
    <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-sm bg-gray-50 rounded p-2 mt-2">
      <div><p className="text-xs text-gray-500">Target</p><p className="font-medium">{formatThb(funding.targetAmount)}</p></div>
      <div><p className="text-xs text-gray-500">Designated funding</p><p className="font-medium">{formatThb(funding.designatedFunding)}</p></div>
      <div><p className="text-xs text-gray-500">Goal progress</p><p className="font-medium">{Math.round(funding.progressPercent as number)}%</p></div>
      <div><p className="text-xs text-gray-500">Funding gap</p><p className="font-medium">{formatThb(funding.fundingGap as number)}</p></div>
    </div>
  );
}

function FundingHealthRow({ health }: { health: SourceFundingHealth }) {
  if (health.status === "UNAVAILABLE") {
    return <p className="text-xs text-gray-400 mt-0.5">Current value unavailable · Funding health unavailable</p>;
  }
  if (health.status === "OVER_ALLOCATED") {
    return (
      <p className="text-xs text-amber-600 mt-0.5">
        Current value {formatThb(health.currentValue as number)} · Attention: exceeds current value by {formatThb(health.shortfall as number)}
      </p>
    );
  }
  return <p className="text-xs text-gray-500 mt-0.5">Current value {formatThb(health.currentValue as number)} · Funding health: Supported</p>;
}

function FundingSourcesSection({
  goalId,
  cashAccounts,
  portfolios,
  allocations,
  onReload,
  fundingHealthForSource,
}: {
  goalId: number;
  cashAccounts: CashAccount[];
  portfolios: Portfolio[];
  allocations: AllocationsState;
  onReload: () => Promise<void>;
  fundingHealthForSource: (kind: GoalFundingSourceKind, id: number) => SourceFundingHealth;
}) {
  const [formError, setFormError] = useState("");

  const [sourceKind, setSourceKind] = useState<GoalFundingSourceKind>("CASH_ACCOUNT");
  const [sourceId, setSourceId] = useState("");
  const [amount, setAmount] = useState("");

  const [editingId, setEditingId] = useState<number | null>(null);
  const [editAmount, setEditAmount] = useState("");

  async function handleAdd(event: FormEvent) {
    event.preventDefault();
    setFormError("");
    const parsed = Number(amount);
    if (!sourceId || !Number.isFinite(parsed) || parsed <= 0) {
      setFormError("Choose a source and enter a positive designated amount.");
      return;
    }
    try {
      await createGoalFundingAllocation(goalId, {
        cash_account_id: sourceKind === "CASH_ACCOUNT" ? Number(sourceId) : undefined,
        portfolio_id: sourceKind === "PORTFOLIO" ? Number(sourceId) : undefined,
        allocated_amount: parsed,
        currency: "THB",
      });
      setSourceId("");
      setAmount("");
      await onReload();
    } catch (err) {
      setFormError(messageFor(err, "Unable to add funding source."));
    }
  }

  async function handleSaveEdit(allocationId: number) {
    setFormError("");
    const parsed = Number(editAmount);
    if (!Number.isFinite(parsed) || parsed <= 0) {
      setFormError("Enter a positive designated amount.");
      return;
    }
    try {
      await updateGoalFundingAllocation(goalId, allocationId, { allocated_amount: parsed });
      setEditingId(null);
      await onReload();
    } catch (err) {
      setFormError(messageFor(err, "Unable to update funding source."));
    }
  }

  async function handleRemove(allocationId: number) {
    setFormError("");
    try {
      await deleteGoalFundingAllocation(goalId, allocationId);
      await onReload();
    } catch (err) {
      setFormError(messageFor(err, "Unable to remove funding source."));
    }
  }

  const sourceOptions: { id: number; name: string }[] = sourceKind === "CASH_ACCOUNT" ? cashAccounts : portfolios;

  return (
    <div className="pt-3 border-t space-y-2">
      <p className="text-sm font-medium text-gray-700">Funding sources</p>

      {allocations === undefined ? (
        <p className="text-xs text-gray-400">Loading funding sources…</p>
      ) : !Array.isArray(allocations) ? (
        <p role="alert" className="text-xs text-red-600">{allocations.error}</p>
      ) : allocations.length === 0 ? (
        <p className="text-xs text-gray-500">No funding sources designated yet.</p>
      ) : (
        <ul className="space-y-1.5">
          {allocations.map((allocation) => {
            const allocationSourceId = (allocation.cash_account_id ?? allocation.portfolio_id) as number;
            const health = fundingHealthForSource(allocation.source_kind, allocationSourceId);
            return (
              <li key={allocation.id} className="text-sm border-b last:border-0 pb-1.5">
                <div className="flex items-center justify-between gap-2 flex-wrap">
                  <span className="text-gray-700">
                    {allocation.source_name ?? "Unknown source"}{" "}
                    <span className="text-xs text-gray-400 ml-1">
                      ({allocation.source_kind === "CASH_ACCOUNT" ? "Cash Account" : "Portfolio"}
                      {allocation.source_is_archived ? ", archived" : ""})
                    </span>
                  </span>
                  {editingId === allocation.id ? (
                    <span className="flex items-center gap-1.5">
                      <input
                        aria-label={`Edit designated amount for ${allocation.source_name ?? "source"}`}
                        type="number"
                        step="0.01"
                        value={editAmount}
                        onChange={(event) => setEditAmount(event.target.value)}
                        className="w-28 border rounded px-2 py-1 text-sm"
                      />
                      <button type="button" onClick={() => void handleSaveEdit(allocation.id)} className="text-blue-600 hover:underline text-xs">Save</button>
                      <button type="button" onClick={() => setEditingId(null)} className="text-gray-500 hover:underline text-xs">Cancel</button>
                    </span>
                  ) : (
                    <span className="flex items-center gap-2">
                      <span className="font-medium">{formatThb(allocation.allocated_amount)} designated</span>
                      <button
                        type="button"
                        aria-label={`Edit designated amount for ${allocation.source_name ?? "source"}`}
                        onClick={() => { setEditingId(allocation.id); setEditAmount(String(allocation.allocated_amount)); }}
                        className="text-blue-600 hover:underline text-xs"
                      >
                        Edit
                      </button>
                      <button
                        type="button"
                        aria-label={`Remove ${allocation.source_name ?? "source"} as a funding source`}
                        onClick={() => void handleRemove(allocation.id)}
                        className="text-red-600 hover:underline text-xs"
                      >
                        Remove
                      </button>
                    </span>
                  )}
                </div>
                <FundingHealthRow health={health} />
              </li>
            );
          })}
        </ul>
      )}

      {formError && <p role="alert" className="text-xs text-red-600">{formError}</p>}

      <form onSubmit={handleAdd} className="flex items-end gap-2 flex-wrap pt-1">
        <label className="text-xs text-gray-500">
          Source kind
          <select
            aria-label="Funding source kind"
            value={sourceKind}
            onChange={(event) => { setSourceKind(event.target.value as GoalFundingSourceKind); setSourceId(""); }}
            className="block border rounded px-2 py-1 text-sm mt-0.5"
          >
            <option value="CASH_ACCOUNT">Cash Account</option>
            <option value="PORTFOLIO">Portfolio</option>
          </select>
        </label>
        <label className="text-xs text-gray-500">
          Source
          <select
            aria-label="Funding source"
            value={sourceId}
            onChange={(event) => setSourceId(event.target.value)}
            className="block border rounded px-2 py-1 text-sm mt-0.5 min-w-[10rem]"
          >
            <option value="">Select…</option>
            {sourceOptions.map((source) => <option key={source.id} value={source.id}>{source.name}</option>)}
          </select>
        </label>
        <label className="text-xs text-gray-500">
          Designated amount
          <input
            aria-label="Designated amount"
            type="number"
            step="0.01"
            value={amount}
            onChange={(event) => setAmount(event.target.value)}
            className="block border rounded px-2 py-1 text-sm mt-0.5 w-32"
          />
        </label>
        <button type="submit" className="bg-blue-600 text-white px-3 py-1.5 rounded text-sm hover:bg-blue-700">Add funding source</button>
      </form>
    </div>
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
