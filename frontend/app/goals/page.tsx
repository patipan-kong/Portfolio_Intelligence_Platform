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
  type GoalContextState as GoalContextViewState,
} from "@/components/goals/GoalPlanningSections";
import {
  buildSourceFundingOverview,
  factualReviewMatchesGoalContext,
  type SourceFundingOverviewRow,
} from "@/lib/goalFunding";
import {
  createWealthGoal,
  getWealthFactualReview,
  listWealthGoals,
  updateWealthGoal,
  type FactualReviewResponse,
  type GoalContextGoal,
  type GoalContextResponse,
  type WealthGoal,
  type WealthGoalPriority,
  type WealthGoalType,
} from "@/lib/api";

type GoalContextLoadError = { error: string };
type WorkspaceReviewState = FactualReviewResponse | GoalContextLoadError | undefined;

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

function goalRecordMatchesContext(record: WealthGoal, contextGoal: GoalContextGoal): boolean {
  return record.id === contextGoal.id
    && record.name === contextGoal.name
    && record.goal_type === contextGoal.goal_type
    && record.target_amount === contextGoal.target_amount
    && record.currency === contextGoal.currency
    && record.target_date === contextGoal.target_date
    && record.priority === contextGoal.priority
    && record.is_archived === contextGoal.is_archived
    && record.updated_at === contextGoal.updated_at;
}

export default function GoalsPage() {
  const [goals, setGoals] = useState<WealthGoal[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [mutationError, setMutationError] = useState("");
  const [showArchived, setShowArchived] = useState(false);
  const [factualReview, setFactualReview] = useState<WorkspaceReviewState>(undefined);

  const refreshGenerationRef = useRef(0);
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

  // One coherent, generation-guarded refresh: fetch the editable goal records
  // and the complete workspace Goal Context together. The archive toggle is
  // presentation-only and never triggers another read. Goal Context is the
  // sole source for progress, allocations, and designation aggregates.
  const refresh = useCallback(async () => {
    const generation = ++refreshGenerationRef.current;
    const isCurrent = () => mountedRef.current && refreshGenerationRef.current === generation;
    setLoading(true);
    setError("");
    setFactualReview(undefined);

    const [goalsResult, contextResult] = await Promise.allSettled([
      listWealthGoals(true),
      getWealthFactualReview(true),
    ]);
    if (!isCurrent()) return;
    if (goalsResult.status === "rejected") {
      setGoals([]);
      setFactualReview(undefined);
      setError(messageFor(goalsResult.reason, "Unable to load goals."));
      setLoading(false);
      return;
    }

    const loadedGoals = goalsResult.value;
    setGoals(loadedGoals);
    if (contextResult.status === "fulfilled") {
      setFactualReview(contextResult.value);
    } else {
      setFactualReview({ error: messageFor(contextResult.reason, "Unable to load factual wealth review.") });
    }
    setLoading(false);
  }, []);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  const active = goals.filter((item) => !item.is_archived);
  const archived = goals.filter((item) => item.is_archived);

  const reviewResponse = factualReview && "goal_context" in factualReview ? factualReview : null;
  const contextResponse = reviewResponse?.goal_context ?? null;
  const contextMatchesGoals = contextResponse !== null
    && reviewResponse?.contract_version === "wealth.factual-review.v1"
    && reviewResponse.scope.kind === "WORKSPACE"
    && reviewResponse.scope.include_archived === true
    && factualReviewMatchesGoalContext(reviewResponse)
    && contextResponse.contract_version === "wealth.goal-context.v1"
    && contextResponse.completeness === "COMPLETE"
    && contextResponse.scope.kind === "WORKSPACE"
    && contextResponse.scope.include_archived === true
    && contextResponse.goals.length === goals.length
    && goals.every((item) => {
      const contextGoal = contextResponse.goals.find((candidate) => candidate.id === item.id);
      return contextGoal !== undefined && goalRecordMatchesContext(item, contextGoal);
    });
  const contextError = factualReview && "error" in factualReview
    ? factualReview.error
    : contextResponse && !contextMatchesGoals
      ? "Goal Context does not match the current goal records."
      : "";

  const contextByGoal = useMemo(() => {
    const map = new Map<number, GoalContextGoal>();
    if (contextResponse && contextMatchesGoals) {
      for (const contextGoal of contextResponse.goals) map.set(contextGoal.id, contextGoal);
    }
    return map;
  }, [contextMatchesGoals, contextResponse]);

  const goalContextFor = useCallback((goalId: number): GoalContextViewState => {
    if (factualReview === undefined) return undefined;
    if (contextError) return { error: contextError };
    return contextByGoal.get(goalId) ?? { error: "Goal Context is unavailable for this goal." };
  }, [contextByGoal, contextError, factualReview]);

  const overviewRows: SourceFundingOverviewRow[] = useMemo(
    () => buildSourceFundingOverview(contextMatchesGoals ? reviewResponse?.sources ?? [] : []),
    [contextMatchesGoals, reviewResponse]
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
            <GoalCard key={item.id} item={item} goalContext={goalContextFor(item.id)} onEdit={openEdit} onArchive={() => void setArchived(item, true)} />
          ))}</div>
        )}
      </section>

      <section className="space-y-3 pt-2 border-t" aria-labelledby="factual-wealth-review-heading">
        <h2 className="text-lg font-semibold" id="factual-wealth-review-heading">Factual wealth review</h2>
        {loading || factualReview === undefined ? (
          <p className="text-sm text-gray-400">Loading factual wealth review…</p>
        ) : error || contextError || !reviewResponse || !contextMatchesGoals ? (
          <p role="alert" className="text-sm text-red-600">
            Factual wealth review is unavailable — Goal Context evidence is incomplete.
          </p>
        ) : (
          <FactualWealthReviewSummary review={reviewResponse} />
        )}
      </section>

      <section className="space-y-3 pt-2 border-t" aria-labelledby="funding-source-health-heading">
        <h2 id="funding-source-health-heading" className="text-lg font-semibold">Funding source health</h2>
        {loading || factualReview === undefined ? (
          <p className="text-sm text-gray-400">Loading funding source health…</p>
        ) : error || contextError || !contextResponse || !contextMatchesGoals ? (
          <p role="alert" className="text-sm text-red-600">
            Funding source health is unavailable — Goal Context evidence is incomplete.
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
  goalContext,
  onEdit,
  onArchive,
}: {
  item: WealthGoal;
  goalContext: GoalContextViewState;
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
      <GoalFundingSummary goalContext={goalContext} compact />
    </article>
  );
}

function SourceHealthRow({ row }: { row: SourceFundingOverviewRow }) {
  const evidence = row.health.provenance === "PORTFOLIO_SNAPSHOT"
    ? `Portfolio snapshot${row.health.asOf ? ` as of ${row.health.asOf}` : ""}`
    : row.health.provenance === "CASH_ACCOUNT_CURRENT_BALANCE"
      ? `Cash account balance${row.health.asOf ? ` as of ${row.health.asOf}` : ""}`
      : "Valuation evidence unavailable";
  const quality = row.health.quality ? ` · Quality: ${row.health.quality}` : "";
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
        <p className="text-xs text-gray-400 mt-0.5">
          {row.health.currentValue === null ? "Observed value unavailable" : `Observed value ${formatThb(row.health.currentValue)}`} · Funding health unavailable · {evidence}{quality}
        </p>
      ) : row.health.status === "OVER_ALLOCATED" ? (
        <p className="text-xs text-amber-600 mt-0.5">
          Observed value {formatThb(row.health.currentValue as number)} · Over-allocated by {formatThb(row.health.shortfall as number)} · {evidence}{quality}
        </p>
      ) : (
        <p className="text-xs text-gray-500 mt-0.5">Observed value {formatThb(row.health.currentValue as number)} · Funding health: Supported · {evidence}{quality}</p>
      )}
    </li>
  );
}

function FactualWealthReviewSummary({ review }: { review: FactualReviewResponse }) {
  if (review.sources.length === 0) {
    return <p className="text-sm text-gray-500">No funding sources are designated, so no valuation evidence is required.</p>;
  }

  if (review.valuation_completeness === "COMPLETE") {
    return <p className="text-sm text-gray-600">Valuation evidence is complete for all designated funding sources.</p>;
  }

  if (review.valuation_completeness === "PARTIAL") {
    return <p className="text-sm text-amber-700">Valuation evidence is partial. Review each funding source’s availability and quality below.</p>;
  }

  return <p className="text-sm text-red-600">Valuation evidence is unavailable for the designated funding sources.</p>;
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
