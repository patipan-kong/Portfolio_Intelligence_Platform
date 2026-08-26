"use client";

import { FormEvent, useState } from "react";
import {
  computeGoalFunding,
  computeSourceFundingHealth,
  type SourceFundingHealth,
} from "@/lib/goalFunding";
import {
  computeGoalWhatIf,
  computeRequiredMonthlyContribution,
  formatMonthLabel,
} from "@/lib/goalWhatIf";
import {
  createGoalFundingAllocation,
  deleteGoalFundingAllocation,
  updateGoalFundingAllocation,
  updateGoalScenario,
  type CashAccount,
  type GoalFundingAllocation,
  type GoalFundingSourceKind,
  type GoalScenario,
  type Portfolio,
  type WealthGoal,
  type WealthGoalPriority,
  type WealthGoalType,
} from "@/lib/api";

export interface AllocationsLoadError {
  error: string;
}

export type AllocationsState = GoalFundingAllocation[] | AllocationsLoadError | undefined;

export interface ScenariosLoadError {
  error: string;
}

export type ScenariosState = GoalScenario[] | ScenariosLoadError | undefined;

export const SAVED_SCENARIO_DISCLOSURE =
  "Saved scenarios store assumptions only. Results use the goal's current target and designated funding.";

/** The transient forward What-If assumptions, lifted above GoalWhatIfSection
 * so loading a saved Scenario can populate them from outside. */
export interface WhatIfAssumptionsState {
  expanded: boolean;
  setExpanded: (value: boolean) => void;
  mode: "forward" | "required";
  setMode: (value: "forward" | "required") => void;
  monthlyContribution: string;
  setMonthlyContribution: (value: string) => void;
  annualReturnPct: string;
  setAnnualReturnPct: (value: string) => void;
}

export const inputClass = "mt-1 block w-full border rounded px-3 py-2";

export const typeLabel = (value: WealthGoalType) => ({
  RETIREMENT: "Retirement",
  HOUSE: "House",
  WEDDING: "Wedding",
  EDUCATION: "Education",
  VACATION: "Vacation",
  EMERGENCY_FUND: "Emergency fund",
  FIRE: "FIRE",
  OTHER: "Other",
}[value]);

export const priorityLabel = (value: WealthGoalPriority) => ({
  HIGH: "High",
  MEDIUM: "Medium",
  LOW: "Low",
}[value]);

export const formatThb = (value: number) => value.toLocaleString("th-TH", {
  style: "currency",
  currency: "THB",
  minimumFractionDigits: 2,
});

export const messageFor = (error: unknown, fallback: string) => error instanceof Error ? error.message : fallback;

export type FundingHealthForSource = (kind: GoalFundingSourceKind, id: number) => SourceFundingHealth;

export function GoalSummary({
  item,
  allocations,
  compact = false,
}: {
  item: WealthGoal;
  allocations: AllocationsState;
  compact?: boolean;
}) {
  return (
    <section className={compact ? "space-y-2" : "space-y-3"} aria-label={`${item.name} goal summary`}>
      <div className="flex items-start justify-between gap-4 flex-wrap">
        <div>
          <p className={compact ? "font-semibold" : "text-xl font-semibold"}>{item.name}</p>
          <p className="text-sm text-gray-500">{typeLabel(item.goal_type)} · {priorityLabel(item.priority)} priority</p>
          <p className={compact ? "text-base font-medium mt-1" : "text-lg font-medium mt-1"}>
            {formatThb(item.target_amount)} <span className="text-xs text-gray-500">target</span>
          </p>
          <p className="text-xs text-gray-400 mt-1">
            {item.target_date ? `Target date: ${item.target_date}` : "No target date set"}
          </p>
          {!compact && item.note && <p className="text-sm text-gray-500 mt-1">{item.note}</p>}
        </div>
      </div>
      <GoalFundingSummary allocations={allocations} targetAmount={item.target_amount} compact={compact} />
    </section>
  );
}

export function GoalFundingSummary({
  allocations,
  targetAmount,
  compact = false,
}: {
  allocations: AllocationsState;
  targetAmount: number;
  compact?: boolean;
}) {
  if (allocations === undefined) {
    return <p className="text-xs text-gray-400">Loading funding progress…</p>;
  }
  const funding = computeGoalFunding(targetAmount, Array.isArray(allocations) ? allocations : null);
  if (funding.designatedFunding === null) {
    return <p role="alert" className="text-xs text-red-600">Goal progress unavailable — funding data failed to load.</p>;
  }
  return (
    <div className={`${compact ? "grid grid-cols-2 sm:grid-cols-3 text-xs" : "grid grid-cols-2 sm:grid-cols-4 text-sm"} gap-2 bg-gray-50 rounded p-2`}>
      {!compact && <div><p className="text-xs text-gray-500">Target</p><p className="font-medium">{formatThb(funding.targetAmount)}</p></div>}
      <div><p className="text-xs text-gray-500">Designated funding</p><p className="font-medium">{formatThb(funding.designatedFunding)}</p></div>
      <div><p className="text-xs text-gray-500">Goal progress</p><p className="font-medium">{Math.round(funding.progressPercent as number)}%</p></div>
      <div><p className="text-xs text-gray-500">Funding gap</p><p className="font-medium">{formatThb(funding.fundingGap as number)}</p></div>
    </div>
  );
}

export function FundingHealthRow({ health }: { health: SourceFundingHealth }) {
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

export function FundingSourcesSection({
  goalId,
  readOnly = false,
  cashAccounts,
  portfolios,
  allocations,
  onReload,
  fundingHealthForSource,
}: {
  goalId: number;
  readOnly?: boolean;
  cashAccounts: CashAccount[];
  portfolios: Portfolio[];
  allocations: AllocationsState;
  onReload: () => Promise<void>;
  fundingHealthForSource: FundingHealthForSource;
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
    <section className="pt-3 border-t space-y-2" aria-labelledby="funding-sources-heading">
      <h3 id="funding-sources-heading" className="text-base font-semibold text-gray-800">Funding Sources</h3>

      {allocations === undefined ? (
        <p className="text-sm text-gray-400">Loading funding sources…</p>
      ) : !Array.isArray(allocations) ? (
        <p role="alert" className="text-sm text-red-600">{allocations.error}</p>
      ) : allocations.length === 0 ? (
        <p className="text-sm text-gray-500">No funding sources designated yet.</p>
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
                      {!readOnly && <>
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
                      </>}
                    </span>
                  )}
                </div>
                <FundingHealthRow health={health} />
              </li>
            );
          })}
        </ul>
      )}

      {formError && <p role="alert" className="text-sm text-red-600">{formError}</p>}

      {readOnly ? <p className="text-sm text-gray-500">Funding sources are read-only while this goal is archived.</p> : <form onSubmit={handleAdd} className="flex items-end gap-2 flex-wrap pt-1">
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
      </form>}
    </section>
  );
}

function todayIso(): string {
  return new Date().toISOString().slice(0, 10);
}

export function GoalWhatIfSection({
  item,
  allocations,
  fundingHealthForSource,
  whatIf,
  readOnly = false,
  onSaveScenario,
}: {
  item: WealthGoal;
  allocations: AllocationsState;
  fundingHealthForSource: FundingHealthForSource;
  whatIf: WhatIfAssumptionsState;
  /** True while the goal is archived — a saved What-If projection can still be viewed, but not saved as a new Scenario. */
  readOnly?: boolean;
  onSaveScenario: (monthlyContribution: number, annualReturnPct: number, name: string) => Promise<void>;
}) {
  const { expanded, setExpanded, mode, setMode, monthlyContribution, setMonthlyContribution, annualReturnPct, setAnnualReturnPct } = whatIf;
  const [savingName, setSavingName] = useState("");
  const [showSaveForm, setShowSaveForm] = useState(false);
  const [saveError, setSaveError] = useState("");
  const [saveConfirmation, setSaveConfirmation] = useState("");

  if (!expanded) {
    return (
      <section className="pt-3 border-t" aria-labelledby={`what-if-heading-${item.id}`}>
        <button id={`what-if-heading-${item.id}`} type="button" onClick={() => setExpanded(true)} className="text-sm text-blue-600 hover:underline">What-If</button>
      </section>
    );
  }

  const funding = computeGoalFunding(item.target_amount, Array.isArray(allocations) ? allocations : null);
  const startingValue = funding.designatedFunding;
  const parsedContribution = monthlyContribution.trim() === "" ? 0 : Number(monthlyContribution);
  const parsedReturn = annualReturnPct.trim() === "" ? 0 : Number(annualReturnPct);
  const result = startingValue === null ? null : computeGoalWhatIf({
    targetAmount: item.target_amount,
    startingValue,
    monthlyContribution: parsedContribution,
    annualReturnPct: parsedReturn,
    asOfDate: todayIso(),
    targetDate: item.target_date,
  });
  const requiredResult = startingValue === null ? null : computeRequiredMonthlyContribution({
    targetAmount: item.target_amount,
    startingValue,
    annualReturnPct: parsedReturn,
    asOfDate: todayIso(),
    targetDate: item.target_date,
  });
  const sourceHealths = Array.isArray(allocations)
    ? allocations
        .map((allocation) => fundingHealthForSource(allocation.source_kind, (allocation.cash_account_id ?? allocation.portfolio_id) as number))
        .filter((health) => health.status !== "SUPPORTED")
    : [];

  return (
    <section className="pt-3 border-t space-y-2" aria-labelledby={`what-if-heading-${item.id}`}>
      <button id={`what-if-heading-${item.id}`} type="button" onClick={() => setExpanded(false)} className="text-sm text-blue-600 hover:underline">What-If</button>
      <div role="group" aria-label={`What-If mode for ${item.name}`} className="flex gap-2 text-xs">
        <button
          type="button"
          aria-pressed={mode === "forward"}
          onClick={() => setMode("forward")}
          className={mode === "forward" ? "font-semibold text-blue-700" : "text-gray-500 hover:underline"}
        >
          When will I reach it?
        </button>
        <button
          type="button"
          aria-pressed={mode === "required"}
          onClick={() => setMode("required")}
          className={mode === "required" ? "font-semibold text-blue-700" : "text-gray-500 hover:underline"}
        >
          How much per month do I need?
        </button>
      </div>

      <div className="grid gap-3 sm:grid-cols-2">
        {mode === "forward" && (
          <Field label="Monthly contribution">
            <input
              aria-label={`What-If monthly contribution for ${item.name}`}
              type="number"
              step="0.01"
              value={monthlyContribution}
              onChange={(event) => setMonthlyContribution(event.target.value)}
              className={inputClass}
            />
          </Field>
        )}
        <Field label="Annual return assumption (%)">
          <input
            aria-label={`What-If annual return assumption for ${item.name}`}
            type="number"
            step="0.01"
            value={annualReturnPct}
            onChange={(event) => setAnnualReturnPct(event.target.value)}
            className={inputClass}
          />
        </Field>
      </div>

      {allocations === undefined ? (
        <p className="text-sm text-gray-400">What-If loading — funding data is still loading.</p>
      ) : startingValue === null ? (
        <p role="alert" className="text-sm text-red-600">What-If unavailable — funding data failed to load.</p>
      ) : mode === "forward" ? (
        !result || !result.valid ? (
          <p role="alert" className="text-sm text-red-600">{result && !result.valid ? result.error : "Invalid What-If inputs."}</p>
        ) : (
          <div className="text-sm bg-gray-50 rounded p-2 space-y-1.5">
            <p className="text-xs text-gray-500">
              Monthly contribution: {formatThb(result.assumptions.monthlyContribution)} · Annual return assumption: {result.assumptions.annualReturnPct}%
            </p>
            {result.alreadyReached ? (
              <p>Designated funding already reaches {formatThb(result.targetAmount)} under these assumptions.</p>
            ) : result.reachable ? (
              <p>Under these assumptions, designated funding would reach {formatThb(result.targetAmount)} around {formatMonthLabel(result.reachDate as string)}.</p>
            ) : (
              <p>Under these assumptions, designated funding would not reach {formatThb(result.targetAmount)} within 50 years.</p>
            )}
            {result.targetDate && (
              result.targetDateInPast ? (
                <p className="text-xs text-gray-500">Saved target date ({result.targetDate}) has passed.</p>
              ) : (
                <p className="text-xs text-gray-500">
                  Saved target date: {result.targetDate} · Projected amount by that date: {formatThb(result.projectedValueAtTargetDate as number)}
                  {result.shortfallAtTargetDate != null && ` · ${formatThb(result.shortfallAtTargetDate)} below the current target`}
                  {result.surplusAtTargetDate != null && ` · ${formatThb(result.surplusAtTargetDate)} above the current target`}
                </p>
              )
            )}
          </div>
        )
      ) : !requiredResult || !requiredResult.valid ? (
        <p role="alert" className="text-sm text-red-600">{requiredResult && !requiredResult.valid ? requiredResult.error : "Invalid required-contribution inputs."}</p>
      ) : (
        <div className="text-sm bg-gray-50 rounded p-2 space-y-1.5">
          <p className="text-xs text-gray-500">
            Designated funding starting amount: {formatThb(requiredResult.startingValue)} · Current target: {formatThb(requiredResult.targetAmount)}
          </p>
          <p className="text-xs text-gray-500">
            Saved target date: {requiredResult.assumptions.targetDate} · Annual return assumption: {requiredResult.assumptions.annualReturnPct}%
          </p>
          {requiredResult.alreadyReached ? (
            <p>No additional monthly contribution is required under the current designated funding.</p>
          ) : (
            <p>Under this assumption, contributing {formatThb(requiredResult.requiredMonthlyContribution)} per month would reach the current target by {requiredResult.assumptions.targetDate}.</p>
          )}
          <p className="text-xs text-gray-500">Projected amount by that date: {formatThb(requiredResult.projectedValueAtTargetDate)}</p>
        </div>
      )}

      {!readOnly && mode === "forward" && result && result.valid && (
        <div className="pt-1 border-t">
          {!showSaveForm ? (
            <button
              type="button"
              onClick={() => { setShowSaveForm(true); setSaveError(""); setSaveConfirmation(""); }}
              className="text-xs text-blue-600 hover:underline"
            >
              Save scenario
            </button>
          ) : (
            <form
              className="flex items-end gap-2 flex-wrap pt-1"
              onSubmit={async (event) => {
                event.preventDefault();
                setSaveError("");
                if (!savingName.trim()) {
                  setSaveError("Enter a name for this scenario.");
                  return;
                }
                try {
                  await onSaveScenario(parsedContribution, parsedReturn, savingName.trim());
                  setShowSaveForm(false);
                  setSavingName("");
                  setSaveConfirmation("Scenario saved.");
                } catch (err) {
                  setSaveError(messageFor(err, "Unable to save scenario."));
                }
              }}
            >
              <label className="text-xs text-gray-500">
                Scenario name
                <input
                  aria-label={`Scenario name for ${item.name}`}
                  type="text"
                  value={savingName}
                  onChange={(event) => setSavingName(event.target.value)}
                  className="block border rounded px-2 py-1 text-sm mt-0.5"
                />
              </label>
              <button type="submit" className="bg-blue-600 text-white px-3 py-1.5 rounded text-sm hover:bg-blue-700">Save</button>
              <button type="button" onClick={() => { setShowSaveForm(false); setSaveError(""); }} className="text-gray-500 hover:underline text-xs">Cancel</button>
            </form>
          )}
          {saveError && <p role="alert" className="text-xs text-red-600 mt-1">{saveError}</p>}
          {saveConfirmation && <p className="text-xs text-gray-500 mt-1">{saveConfirmation}</p>}
        </div>
      )}

      {sourceHealths.length > 0 && (
        <div className="pt-1 border-t">
          <p className="text-xs text-gray-500">Funding health for this goal&apos;s sources:</p>
          {sourceHealths.map((health, index) => <FundingHealthRow key={index} health={health} />)}
        </div>
      )}
    </section>
  );
}

export function SavedScenariosSection({
  goalId,
  readOnly = false,
  scenarios,
  onReload,
  onLoadScenario,
}: {
  goalId: number;
  /** True while the goal is archived — create/edit/archive/restore are disabled; loading is still allowed. */
  readOnly?: boolean;
  scenarios: ScenariosState;
  onReload: () => Promise<void>;
  onLoadScenario: (scenario: GoalScenario) => void;
}) {
  const [formError, setFormError] = useState("");
  const [showArchived, setShowArchived] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editName, setEditName] = useState("");
  const [editContribution, setEditContribution] = useState("");
  const [editReturn, setEditReturn] = useState("");

  function startEdit(scenario: GoalScenario) {
    setFormError("");
    setEditingId(scenario.id);
    setEditName(scenario.name);
    setEditContribution(String(scenario.monthly_contribution));
    setEditReturn(String(scenario.annual_return_pct));
  }

  async function handleSaveEdit(scenarioId: number) {
    setFormError("");
    const parsedContribution = Number(editContribution);
    const parsedReturn = Number(editReturn);
    if (!editName.trim()) {
      setFormError("Enter a name for this scenario.");
      return;
    }
    if (!Number.isFinite(parsedContribution) || parsedContribution < 0) {
      setFormError("Enter a monthly contribution of zero or more.");
      return;
    }
    if (!Number.isFinite(parsedReturn) || parsedReturn <= -100) {
      setFormError("Enter an annual return assumption greater than -100%.");
      return;
    }
    try {
      await updateGoalScenario(goalId, scenarioId, {
        name: editName.trim(),
        monthly_contribution: parsedContribution,
        annual_return_pct: parsedReturn,
      });
      setEditingId(null);
      await onReload();
    } catch (err) {
      setFormError(messageFor(err, "Unable to update scenario."));
    }
  }

  async function handleArchiveToggle(scenario: GoalScenario) {
    setFormError("");
    try {
      await updateGoalScenario(goalId, scenario.id, { is_archived: !scenario.is_archived });
      await onReload();
    } catch (err) {
      setFormError(messageFor(err, "Unable to update scenario."));
    }
  }

  const rows = Array.isArray(scenarios) ? scenarios : [];
  const activeRows = rows.filter((row) => !row.is_archived);
  const archivedRows = rows.filter((row) => row.is_archived);

  return (
    <section className="space-y-2" aria-labelledby="saved-scenarios-heading">
      <p className="text-xs text-gray-500">{SAVED_SCENARIO_DISCLOSURE}</p>

      {scenarios === undefined ? (
        <p className="text-sm text-gray-400">Loading saved scenarios…</p>
      ) : !Array.isArray(scenarios) ? (
        <p role="alert" className="text-sm text-red-600">{scenarios.error}</p>
      ) : activeRows.length === 0 ? (
        <p className="text-sm text-gray-500">No saved scenarios yet.</p>
      ) : (
        <ul className="space-y-1.5">
          {activeRows.map((scenario) => (
            <li key={scenario.id} className="text-sm border-b last:border-0 pb-1.5">
              {editingId === scenario.id ? (
                <div className="flex items-end gap-2 flex-wrap">
                  <label className="text-xs text-gray-500">
                    Name
                    <input
                      aria-label={`Edit name for ${scenario.name}`}
                      type="text"
                      value={editName}
                      onChange={(event) => setEditName(event.target.value)}
                      className="block border rounded px-2 py-1 text-sm mt-0.5"
                    />
                  </label>
                  <label className="text-xs text-gray-500">
                    Monthly contribution
                    <input
                      aria-label={`Edit monthly contribution for ${scenario.name}`}
                      type="number"
                      step="0.01"
                      value={editContribution}
                      onChange={(event) => setEditContribution(event.target.value)}
                      className="w-28 border rounded px-2 py-1 text-sm mt-0.5"
                    />
                  </label>
                  <label className="text-xs text-gray-500">
                    Annual return (%)
                    <input
                      aria-label={`Edit annual return assumption for ${scenario.name}`}
                      type="number"
                      step="0.01"
                      value={editReturn}
                      onChange={(event) => setEditReturn(event.target.value)}
                      className="w-20 border rounded px-2 py-1 text-sm mt-0.5"
                    />
                  </label>
                  <button type="button" onClick={() => void handleSaveEdit(scenario.id)} className="text-blue-600 hover:underline text-xs">Save</button>
                  <button type="button" onClick={() => setEditingId(null)} className="text-gray-500 hover:underline text-xs">Cancel</button>
                </div>
              ) : (
                <div className="flex items-center justify-between gap-2 flex-wrap">
                  <span className="text-gray-700">
                    <span className="font-medium">{scenario.name}</span>{" "}
                    <span className="text-xs text-gray-400">
                      ({formatThb(scenario.monthly_contribution)}/month · {scenario.annual_return_pct}% annual return assumption)
                    </span>
                  </span>
                  <span className="flex items-center gap-2">
                    <button type="button" aria-label={`Load ${scenario.name} scenario`} onClick={() => onLoadScenario(scenario)} className="text-blue-600 hover:underline text-xs">Load</button>
                    {!readOnly && <>
                      <button type="button" aria-label={`Edit ${scenario.name} scenario`} onClick={() => startEdit(scenario)} className="text-blue-600 hover:underline text-xs">Edit</button>
                      <button type="button" aria-label={`Archive ${scenario.name} scenario`} onClick={() => void handleArchiveToggle(scenario)} className="text-red-600 hover:underline text-xs">Archive</button>
                    </>}
                  </span>
                </div>
              )}
            </li>
          ))}
        </ul>
      )}

      {formError && <p role="alert" className="text-sm text-red-600">{formError}</p>}

      {Array.isArray(scenarios) && archivedRows.length > 0 && (
        <div className="pt-1">
          <button type="button" onClick={() => setShowArchived((value) => !value)} className="text-xs text-blue-600 hover:underline">
            {showArchived ? "Hide archived scenarios" : `Show archived scenarios (${archivedRows.length})`}
          </button>
          {showArchived && (
            <ul className="space-y-1.5 pt-1.5">
              {archivedRows.map((scenario) => (
                <li key={scenario.id} className="text-sm border-b last:border-0 pb-1.5">
                  <div className="flex items-center justify-between gap-2 flex-wrap">
                    <span className="text-gray-700">
                      <span className="font-medium">{scenario.name}</span>{" "}
                      <span className="text-xs text-gray-400">
                        ({formatThb(scenario.monthly_contribution)}/month · {scenario.annual_return_pct}% annual return assumption, archived)
                      </span>
                    </span>
                    <span className="flex items-center gap-2">
                      <button type="button" aria-label={`Load ${scenario.name} scenario`} onClick={() => onLoadScenario(scenario)} className="text-blue-600 hover:underline text-xs">Load</button>
                      {!readOnly && (
                        <button type="button" aria-label={`Restore ${scenario.name} scenario`} onClick={() => void handleArchiveToggle(scenario)} className="text-blue-600 hover:underline text-xs">Restore</button>
                      )}
                    </span>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </section>
  );
}

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return <label className="text-sm">{label}{children}</label>;
}
