"use client";

import { FormEvent, useCallback, useEffect, useMemo, useRef, useState } from "react";
import Link from "next/link";
import {
  createCashAccountTransfer,
  createCashAccountTransaction,
  createCashEntryTemplate,
  createCashInvestmentTransfer,
  deleteCashEntryTemplate,
  getCashFlowReport,
  getCashFlowSettings,
  updateCashFlowSettings,
  updateCashEntryTemplate,
  listCashAccounts,
  listCashEntryTemplates,
  listPortfolios,
  type CashAccount,
  type CashEntryTemplate,
  type CashFlowEvent,
  type CashFlowSettings,
  type Portfolio,
} from "@/lib/api";
import {
  aggregateMonthlyCashFlow,
  currentMonthKey,
  formatMonthLabel,
  shiftMonth,
  signedPresentationAmount,
} from "@/lib/cashFlow";
import {
  computeCoveragePopulation,
  computeCoverageGap,
  computeRecordedExpenseCoverage,
  type MonthlyFetchResult,
  type RecordedExpenseCoverageResult,
} from "@/lib/emergencyFund";
import {
  computeCashFlowTrend,
  computeTrendPopulation,
  DEFAULT_TREND_WINDOW_SIZE,
  TREND_WINDOW_SIZES,
  type CashFlowTrendResult,
  type TrendWindowSize,
} from "@/lib/cashFlowTrend";
import CashFlowTrendChart from "@/components/CashFlowTrendChart";

type EntryType = "INCOME" | "EXPENSE";

const inputClass = "mt-1 block w-full border rounded px-3 py-2";
const formatThb = (value: number) =>
  value.toLocaleString("th-TH", { style: "currency", currency: "THB", minimumFractionDigits: 2 });
const localDateKey = (now = new Date()) =>
  `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, "0")}-${String(now.getDate()).padStart(2, "0")}`;
const messageFor = (error: unknown, fallback: string) => error instanceof Error ? error.message : fallback;

export default function CashFlowPage() {
  const [month, setMonth] = useState(() => currentMonthKey());
  const [report, setReport] = useState<{ month: string; events: CashFlowEvent[] } | null>(null);
  const [reportLoading, setReportLoading] = useState(true);
  const [reportError, setReportError] = useState("");
  const [accounts, setAccounts] = useState<CashAccount[] | null>(null);
  const [accountsLoading, setAccountsLoading] = useState(true);
  const [accountsError, setAccountsError] = useState("");
  const [entryType, setEntryType] = useState<EntryType | null>(null);
  const [entryAccountId, setEntryAccountId] = useState("");
  const [entryAmount, setEntryAmount] = useState("");
  const [entryDate, setEntryDate] = useState(localDateKey());
  const [entryCategory, setEntryCategory] = useState("");
  const [entryNote, setEntryNote] = useState("");
  const [transferOpen, setTransferOpen] = useState(false);
  const [transferSourceId, setTransferSourceId] = useState("");
  const [transferDestinationId, setTransferDestinationId] = useState("");
  const [transferAmount, setTransferAmount] = useState("");
  const [transferDate, setTransferDate] = useState(localDateKey());
  const [transferNote, setTransferNote] = useState("");
  const [portfolios, setPortfolios] = useState<Portfolio[] | null>(null);
  const [portfoliosLoading, setPortfoliosLoading] = useState(true);
  const [portfoliosError, setPortfoliosError] = useState("");
  const [investmentTransferOpen, setInvestmentTransferOpen] = useState(false);
  const [investmentTransferAccountId, setInvestmentTransferAccountId] = useState("");
  const [investmentTransferPortfolioId, setInvestmentTransferPortfolioId] = useState("");
  const [investmentTransferDirection, setInvestmentTransferDirection] = useState<"TO_PORTFOLIO" | "FROM_PORTFOLIO">("TO_PORTFOLIO");
  const [investmentTransferAmount, setInvestmentTransferAmount] = useState("");
  const [investmentTransferDate, setInvestmentTransferDate] = useState(localDateKey());
  const [investmentTransferNote, setInvestmentTransferNote] = useState("");
  const [mutationError, setMutationError] = useState("");
  const [coverage, setCoverage] = useState<RecordedExpenseCoverageResult | null>(null);
  const [coverageLoading, setCoverageLoading] = useState(true);
  const [targetSettings, setTargetSettings] = useState<CashFlowSettings | null>(null);
  const [targetLoading, setTargetLoading] = useState(true);
  const [targetLoadError, setTargetLoadError] = useState("");
  const [targetEditing, setTargetEditing] = useState(false);
  const [targetDraft, setTargetDraft] = useState("");
  const [targetSaving, setTargetSaving] = useState(false);
  const [targetSaveError, setTargetSaveError] = useState("");
  const [trendWindowSize, setTrendWindowSize] = useState<TrendWindowSize>(DEFAULT_TREND_WINDOW_SIZE);
  const [trend, setTrend] = useState<CashFlowTrendResult | null>(null);
  const [trendLoading, setTrendLoading] = useState(true);
  const [templates, setTemplates] = useState<CashEntryTemplate[] | null>(null);
  const [templatesLoading, setTemplatesLoading] = useState(true);
  const [templatesError, setTemplatesError] = useState("");
  const [templateFormOpen, setTemplateFormOpen] = useState(false);
  const [templateEditingId, setTemplateEditingId] = useState<number | null>(null);
  const [templateName, setTemplateName] = useState("");
  const [templateType, setTemplateType] = useState<EntryType>("INCOME");
  const [templateAccountId, setTemplateAccountId] = useState("");
  const [templateAmount, setTemplateAmount] = useState("");
  const [templateCategory, setTemplateCategory] = useState("");
  const [templateNote, setTemplateNote] = useState("");
  const [templateMutationError, setTemplateMutationError] = useState("");
  const reportRequestId = useRef(0);
  const coverageRequestId = useRef(0);
  const trendRequestId = useRef(0);

  const loadReport = useCallback(async (selectedMonth: string) => {
    const requestId = ++reportRequestId.current;
    setReportLoading(true);
    setReportError("");
    setReport(null);
    try {
      const loaded = await getCashFlowReport(selectedMonth);
      if (requestId === reportRequestId.current) setReport(loaded);
    } catch (error) {
      if (requestId === reportRequestId.current) setReportError(messageFor(error, "Unable to load Cash Flow."));
    } finally {
      if (requestId === reportRequestId.current) setReportLoading(false);
    }
  }, []);

  const loadAccounts = useCallback(async () => {
    setAccountsLoading(true);
    setAccountsError("");
    try {
      setAccounts(await listCashAccounts(false));
    } catch (error) {
      setAccountsError(messageFor(error, "Unable to load active cash accounts."));
    } finally {
      setAccountsLoading(false);
    }
  }, []);

  const loadTemplates = useCallback(async () => {
    setTemplatesLoading(true);
    setTemplatesError("");
    try {
      setTemplates(await listCashEntryTemplates());
    } catch (error) {
      setTemplatesError(messageFor(error, "Unable to load templates."));
    } finally {
      setTemplatesLoading(false);
    }
  }, []);

  const loadPortfolios = useCallback(async () => {
    setPortfoliosLoading(true);
    setPortfoliosError("");
    try {
      setPortfolios(await listPortfolios());
    } catch (error) {
      setPortfoliosError(messageFor(error, "Unable to load portfolios."));
    } finally {
      setPortfoliosLoading(false);
    }
  }, []);

  const loadCoverage = useCallback(async (accountsList: CashAccount[] | null, status: "success" | "error") => {
    const requestId = ++coverageRequestId.current;
    setCoverageLoading(true);
    const population = computeCoveragePopulation(status, accountsList ?? [], new Date());
    if (population.recordedMonths.length === 0) {
      if (requestId === coverageRequestId.current) {
        setCoverage(computeRecordedExpenseCoverage(population, []));
        setCoverageLoading(false);
      }
      return;
    }
    const monthlyResults: MonthlyFetchResult[] = await Promise.all(
      population.recordedMonths.map(async (coverageMonth): Promise<MonthlyFetchResult> => {
        try {
          const report = await getCashFlowReport(coverageMonth);
          return { month: coverageMonth, status: "success", events: report.events };
        } catch {
          return { month: coverageMonth, status: "error", events: [] };
        }
      }),
    );
    if (requestId === coverageRequestId.current) {
      setCoverage(computeRecordedExpenseCoverage(population, monthlyResults));
      setCoverageLoading(false);
    }
  }, []);

  const loadTrend = useCallback(async (accountsList: CashAccount[] | null, status: "success" | "error", windowSize: TrendWindowSize) => {
    const requestId = ++trendRequestId.current;
    setTrendLoading(true);
    const population = computeTrendPopulation(status, accountsList ?? [], windowSize, new Date());
    if (population.eligibleMonths.length === 0) {
      if (requestId === trendRequestId.current) {
        setTrend(computeCashFlowTrend(population, []));
        setTrendLoading(false);
      }
      return;
    }
    const monthlyResults: MonthlyFetchResult[] = await Promise.all(
      population.eligibleMonths.map(async (trendMonth): Promise<MonthlyFetchResult> => {
        try {
          const monthlyReport = await getCashFlowReport(trendMonth);
          return { month: trendMonth, status: "success", events: monthlyReport.events };
        } catch {
          return { month: trendMonth, status: "error", events: [] };
        }
      }),
    );
    if (requestId === trendRequestId.current) {
      setTrend(computeCashFlowTrend(population, monthlyResults));
      setTrendLoading(false);
    }
  }, []);

  const loadTargetSettings = useCallback(async () => {
    setTargetLoading(true);
    setTargetLoadError("");
    try {
      setTargetSettings(await getCashFlowSettings());
    } catch (error) {
      setTargetLoadError(messageFor(error, "Unable to load your target."));
    } finally {
      setTargetLoading(false);
    }
  }, []);

  useEffect(() => { void loadReport(month); }, [loadReport, month]);
  useEffect(() => { void loadAccounts(); }, [loadAccounts]);
  useEffect(() => { void loadTemplates(); }, [loadTemplates]);
  useEffect(() => { void loadPortfolios(); }, [loadPortfolios]);
  useEffect(() => { void loadTargetSettings(); }, [loadTargetSettings]);
  useEffect(() => {
    if (accountsLoading) return;
    void loadCoverage(accounts, accountsError ? "error" : "success");
  }, [accountsLoading, accounts, accountsError, loadCoverage]);
  useEffect(() => {
    if (accountsLoading) return;
    void loadTrend(accounts, accountsError ? "error" : "success", trendWindowSize);
  }, [accountsLoading, accounts, accountsError, trendWindowSize, loadTrend]);

  const summary = useMemo(
    () => report ? aggregateMonthlyCashFlow(report.events, month) : null,
    [report, month],
  );
  const currentMonth = currentMonthKey();
  const trackedAccounts = (accounts ?? []).filter((account) => !account.is_archived && Boolean(account.baseline));
  const trackedAccountIds = new Set(trackedAccounts.map((account) => account.id));
  const expenseCategories = summary
    ? Object.entries(summary.expenseCategories).sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    : [];
  const hasAdjustments = summary?.events.some((event) => event.transaction_type === "ADJUSTMENT") ?? false;

  function openEntry(type: EntryType) {
    setMutationError("");
    setEntryType(type);
    setEntryAccountId(String(trackedAccounts[0]?.id ?? ""));
    setEntryAmount("");
    setEntryDate(`${month}-01`);
    setEntryCategory("");
    setEntryNote("");
  }

  function closeEntry() {
    setEntryType(null);
    setMutationError("");
  }

  // Template invocation: opens the SAME Add income / Add expense form with
  // stable fields prefilled. No stored date exists on a template, so the date
  // still uses the current page's fresh default (Section 26) — never a
  // remembered or scheduled date. The user reviews/edits and submits through
  // the existing createCashAccountTransaction path; nothing here creates a
  // transaction by itself.
  function useTemplateForEntry(template: CashEntryTemplate) {
    setMutationError("");
    setEntryType(template.transaction_type);
    setEntryAccountId(String(template.cash_account_id));
    setEntryAmount(String(template.amount));
    setEntryDate(`${month}-01`);
    setEntryCategory(template.category);
    setEntryNote(template.note ?? "");
  }

  function openCreateTemplate() {
    setTemplateMutationError("");
    setTemplateEditingId(null);
    setTemplateName("");
    setTemplateType("INCOME");
    setTemplateAccountId(String((accounts ?? [])[0]?.id ?? ""));
    setTemplateAmount("");
    setTemplateCategory("");
    setTemplateNote("");
    setTemplateFormOpen(true);
  }

  function openEditTemplate(template: CashEntryTemplate) {
    setTemplateMutationError("");
    setTemplateEditingId(template.id);
    setTemplateName(template.name);
    setTemplateType(template.transaction_type);
    // The account selector only lists active accounts (Section 8's editor
    // pattern). An archived template's cash_account_id has no matching
    // option, so start it on the "keep current" sentinel ("") rather than an
    // id the <select> cannot represent — see the "Keep current" option in
    // TemplatesSection and the keepingArchivedAccount branch below.
    setTemplateAccountId(template.cash_account_is_archived ? "" : String(template.cash_account_id));
    setTemplateAmount(String(template.amount));
    setTemplateCategory(template.category);
    setTemplateNote(template.note ?? "");
    setTemplateFormOpen(true);
  }

  function closeTemplateForm() {
    setTemplateFormOpen(false);
    setTemplateEditingId(null);
    setTemplateMutationError("");
  }

  async function handleTemplateSubmit(event: FormEvent) {
    event.preventDefault();
    setTemplateMutationError("");
    const amount = Number(templateAmount);
    // CET-01: editing a template whose account is archived starts the
    // selector on the "keep current" sentinel (""), meaning the user has not
    // chosen to repoint. In that case cash_account_id is omitted from the
    // PATCH entirely (Section 5) so the backend preserves the existing
    // archived association without running active-account validation.
    const keepingArchivedAccount = templateEditingId != null && templateAccountId === "";
    const accountId = keepingArchivedAccount ? null : Number(templateAccountId);
    if (!templateName.trim() ||
      (!keepingArchivedAccount && (!Number.isInteger(accountId) || !(accounts ?? []).some((account) => account.id === accountId))) ||
      !Number.isFinite(amount) || amount <= 0 || !templateCategory.trim()) {
      setTemplateMutationError("Enter a template name, choose an active cash account, and enter a positive amount and category.");
      return;
    }
    try {
      if (templateEditingId != null) {
        await updateCashEntryTemplate(templateEditingId, {
          name: templateName.trim(),
          transaction_type: templateType,
          ...(keepingArchivedAccount ? {} : { cash_account_id: accountId as number }),
          amount,
          category: templateCategory.trim(),
          note: templateNote.trim() || null,
        });
      } else {
        await createCashEntryTemplate({
          name: templateName.trim(),
          transaction_type: templateType,
          cash_account_id: accountId as number,
          amount,
          category: templateCategory.trim(),
          note: templateNote.trim() || null,
        });
      }
      closeTemplateForm();
      await loadTemplates();
    } catch (error) {
      setTemplateMutationError(messageFor(error, "Unable to save template."));
    }
  }

  async function handleDeleteTemplate(id: number) {
    setTemplateMutationError("");
    try {
      await deleteCashEntryTemplate(id);
      await loadTemplates();
    } catch (error) {
      setTemplateMutationError(messageFor(error, "Unable to delete template."));
    }
  }

  function openTransfer() {
    setMutationError("");
    setTransferOpen(true);
    setTransferSourceId(String(trackedAccounts[0]?.id ?? ""));
    setTransferDestinationId(String(trackedAccounts[1]?.id ?? ""));
    setTransferAmount("");
    setTransferDate(`${month}-01`);
    setTransferNote("");
  }

  function closeTransfer() {
    setTransferOpen(false);
    setMutationError("");
  }

  function openInvestmentTransfer() {
    setMutationError("");
    setInvestmentTransferOpen(true);
    setInvestmentTransferAccountId(String(trackedAccounts[0]?.id ?? ""));
    setInvestmentTransferPortfolioId(String((portfolios ?? [])[0]?.id ?? ""));
    setInvestmentTransferDirection("TO_PORTFOLIO");
    setInvestmentTransferAmount("");
    setInvestmentTransferDate(`${month}-01`);
    setInvestmentTransferNote("");
  }

  function closeInvestmentTransfer() {
    setInvestmentTransferOpen(false);
    setMutationError("");
  }

  async function handleEntry(event: FormEvent) {
    event.preventDefault();
    if (!entryType) return;
    setMutationError("");
    const amount = Number(entryAmount);
    const accountId = Number(entryAccountId);
    if (!Number.isInteger(accountId) || !trackedAccounts.some((account) => account.id === accountId) ||
      !entryDate || !Number.isFinite(amount) || amount <= 0 || !entryCategory.trim()) {
      setMutationError("Choose a tracked account and enter a positive amount, date, and category.");
      return;
    }
    try {
      await createCashAccountTransaction(accountId, {
        transaction_type: entryType,
        amount,
        occurred_on: entryDate,
        category: entryCategory.trim(),
        note: entryNote.trim() || null,
      });
      closeEntry();
      await Promise.all([loadReport(month), loadAccounts()]);
    } catch (error) {
      setMutationError(messageFor(error, `Unable to add ${entryType === "INCOME" ? "income" : "expense"}.`));
    }
  }

  async function handleTransfer(event: FormEvent) {
    event.preventDefault();
    setMutationError("");
    const sourceId = Number(transferSourceId);
    const destinationId = Number(transferDestinationId);
    const amount = Number(transferAmount);
    if (!Number.isInteger(sourceId) || !Number.isInteger(destinationId) || sourceId === destinationId ||
      !trackedAccounts.some((account) => account.id === sourceId) ||
      !trackedAccounts.some((account) => account.id === destinationId) ||
      !transferDate || !Number.isFinite(amount) || amount <= 0) {
      setMutationError("Choose two different tracked accounts and enter a positive amount and date.");
      return;
    }
    try {
      await createCashAccountTransfer({
        source_cash_account_id: sourceId,
        destination_cash_account_id: destinationId,
        amount,
        occurred_on: transferDate,
        note: transferNote.trim() || null,
      });
      closeTransfer();
      await Promise.all([loadReport(month), loadAccounts()]);
    } catch (error) {
      setMutationError(messageFor(error, "Unable to transfer cash between accounts."));
    }
  }

  async function handleInvestmentTransfer(event: FormEvent) {
    event.preventDefault();
    setMutationError("");
    const accountId = Number(investmentTransferAccountId);
    const portfolioId = Number(investmentTransferPortfolioId);
    const amount = Number(investmentTransferAmount);
    if (!Number.isInteger(accountId) || !trackedAccounts.some((account) => account.id === accountId) ||
      !Number.isInteger(portfolioId) || !(portfolios ?? []).some((portfolio) => portfolio.id === portfolioId) ||
      !investmentTransferDate || !Number.isFinite(amount) || amount <= 0) {
      setMutationError("Choose a tracked account, a portfolio, and enter a positive amount and date.");
      return;
    }
    try {
      await createCashInvestmentTransfer(accountId, {
        portfolio_id: portfolioId,
        direction: investmentTransferDirection,
        amount,
        occurred_on: investmentTransferDate,
        note: investmentTransferNote.trim() || null,
      });
      closeInvestmentTransfer();
      await Promise.all([loadReport(month), loadAccounts()]);
    } catch (error) {
      setMutationError(messageFor(error, "Unable to record the investment transfer."));
    }
  }

  function openTargetEdit() {
    setTargetSaveError("");
    setTargetDraft(targetSettings?.target_coverage_months != null ? String(targetSettings.target_coverage_months) : "");
    setTargetEditing(true);
  }

  function cancelTargetEdit() {
    setTargetEditing(false);
    setTargetSaveError("");
  }

  async function submitTargetEdit(event: FormEvent) {
    event.preventDefault();
    const months = Number(targetDraft);
    if (!Number.isFinite(months) || months <= 0) {
      setTargetSaveError("Enter a target greater than zero.");
      return;
    }
    setTargetSaving(true);
    setTargetSaveError("");
    try {
      setTargetSettings(await updateCashFlowSettings({ target_coverage_months: months }));
      setTargetEditing(false);
    } catch (error) {
      setTargetSaveError(messageFor(error, "Unable to save your target."));
    } finally {
      setTargetSaving(false);
    }
  }

  async function clearTarget() {
    setTargetSaving(true);
    setTargetSaveError("");
    try {
      setTargetSettings(await updateCashFlowSettings({ target_coverage_months: null }));
    } catch (error) {
      setTargetSaveError(messageFor(error, "Unable to clear your target."));
    } finally {
      setTargetSaving(false);
    }
  }

  return (
    <div className="space-y-6 max-w-4xl">
      <header className="flex items-start justify-between gap-4 flex-wrap">
        <div>
          <h1 className="text-2xl font-bold">Cash Flow</h1>
          <p className="text-sm text-gray-500 mt-1">Monthly income and expenses from your prospective cash ledger.</p>
        </div>
        <Link href="/cash" className="text-sm text-blue-600 hover:underline">Cash Accounts →</Link>
      </header>

      <CoverageSection
        coverage={coverage}
        loading={coverageLoading}
        accountsLoading={accountsLoading}
        // Retry the evidence that actually failed: when the account request is
        // what failed, re-running loadCoverage alone would recompute the same
        // stale failure, so reload accounts and let the coverage effect cascade.
        onRetry={() => {
          if (accountsError) void loadAccounts();
          else void loadCoverage(accounts, "success");
        }}
        targetSettings={targetSettings}
        targetLoading={targetLoading}
        targetLoadError={targetLoadError}
        onRetryTarget={() => void loadTargetSettings()}
        targetEditing={targetEditing}
        targetDraft={targetDraft}
        setTargetDraft={setTargetDraft}
        targetSaving={targetSaving}
        targetSaveError={targetSaveError}
        onOpenTargetEdit={openTargetEdit}
        onCancelTargetEdit={cancelTargetEdit}
        onSubmitTargetEdit={submitTargetEdit}
        onClearTarget={clearTarget}
      />

      <section className="bg-white border rounded-xl p-4 shadow-sm flex items-center justify-between gap-3">
        <button type="button" aria-label="Previous month" onClick={() => setMonth((value) => shiftMonth(value, -1))} className="px-3 py-1.5 border rounded text-sm hover:bg-gray-50">←</button>
        <div className="text-center">
          <p className="text-xs uppercase tracking-wide text-gray-400">Selected month</p>
          <h2 className="text-lg font-semibold" aria-live="polite">{formatMonthLabel(month)}</h2>
        </div>
        <div className="flex items-center gap-2">
          <button type="button" aria-label="Next month" disabled={month >= currentMonth} onClick={() => setMonth((value) => shiftMonth(value, 1))} className="px-3 py-1.5 border rounded text-sm hover:bg-gray-50 disabled:opacity-40 disabled:cursor-not-allowed">→</button>
          {month !== currentMonth && <button type="button" onClick={() => setMonth(currentMonth)} className="text-sm text-blue-600 hover:underline">Today</button>}
        </div>
      </section>

      {reportLoading && <p className="text-sm text-gray-400">Loading Cash Flow…</p>}
      {!reportLoading && reportError && (
        <div role="alert" className="border border-red-200 bg-red-50 rounded-xl p-4 text-sm text-red-700 space-y-2">
          <p>{reportError}</p>
          <button type="button" onClick={() => void loadReport(month)} className="text-blue-700 hover:underline">Try again</button>
        </div>
      )}

      {!reportLoading && !reportError && summary && (
        <>
          <section aria-label="Monthly summary" className="grid gap-3 sm:grid-cols-3">
            <SummaryCard label="Income" value={formatThb(summary.income)} tone="positive" />
            <SummaryCard label="Expenses" value={formatThb(summary.expenses)} tone="negative" />
            <SummaryCard label="Net Cash Flow" value={formatThb(summary.netCashFlow)} tone={summary.netCashFlow > 0 ? "positive" : summary.netCashFlow < 0 ? "negative" : "neutral"} />
          </section>

          {hasAdjustments && (
            <section className="border border-amber-200 bg-amber-50 rounded-xl p-4 text-sm text-amber-900">
              <p><strong>Adjustments:</strong> {formatSigned(summary.adjustments)}</p>
              <p className="text-xs mt-1">Reconciliation evidence is shown separately and is excluded from Income, Expenses, and Net Cash Flow.</p>
            </section>
          )}

          <TrendSection
            trend={trend}
            loading={trendLoading}
            accountsLoading={accountsLoading}
            windowSize={trendWindowSize}
            onWindowSizeChange={setTrendWindowSize}
            onRetry={() => {
              if (accountsError) void loadAccounts();
              else void loadTrend(accounts, "success", trendWindowSize);
            }}
          />

          <TemplatesSection
            templates={templates}
            loading={templatesLoading}
            error={templatesError}
            onRetry={() => void loadTemplates()}
            trackedAccountIds={trackedAccountIds}
            onUse={useTemplateForEntry}
            accounts={accounts ?? []}
            formOpen={templateFormOpen}
            editingId={templateEditingId}
            name={templateName}
            type={templateType}
            accountId={templateAccountId}
            amount={templateAmount}
            category={templateCategory}
            note={templateNote}
            mutationError={templateMutationError}
            onOpenCreate={openCreateTemplate}
            onOpenEdit={openEditTemplate}
            onClose={closeTemplateForm}
            onSubmit={handleTemplateSubmit}
            onDelete={handleDeleteTemplate}
            setName={setTemplateName}
            setType={setTemplateType}
            setAccountId={setTemplateAccountId}
            setAmount={setTemplateAmount}
            setCategory={setTemplateCategory}
            setNote={setTemplateNote}
          />

          <EntrySection
            accounts={trackedAccounts}
            accountsLoading={accountsLoading}
            accountsError={accountsError}
            onRetryAccounts={() => void loadAccounts()}
            entryType={entryType}
            entryAccountId={entryAccountId}
            entryAmount={entryAmount}
            entryDate={entryDate}
            entryCategory={entryCategory}
            entryNote={entryNote}
            mutationError={mutationError}
            onOpen={openEntry}
            onClose={closeEntry}
            onSubmit={handleEntry}
            setEntryAccountId={setEntryAccountId}
            setEntryAmount={setEntryAmount}
            setEntryDate={setEntryDate}
            setEntryCategory={setEntryCategory}
            setEntryNote={setEntryNote}
            transferOpen={transferOpen}
            transferSourceId={transferSourceId}
            transferDestinationId={transferDestinationId}
            transferAmount={transferAmount}
            transferDate={transferDate}
            transferNote={transferNote}
            onOpenTransfer={openTransfer}
            onCloseTransfer={closeTransfer}
            onSubmitTransfer={handleTransfer}
            setTransferSourceId={setTransferSourceId}
            setTransferDestinationId={setTransferDestinationId}
            setTransferAmount={setTransferAmount}
            setTransferDate={setTransferDate}
            setTransferNote={setTransferNote}
            portfolios={portfolios ?? []}
            portfoliosLoading={portfoliosLoading}
            investmentTransferOpen={investmentTransferOpen}
            investmentTransferAccountId={investmentTransferAccountId}
            investmentTransferPortfolioId={investmentTransferPortfolioId}
            investmentTransferDirection={investmentTransferDirection}
            investmentTransferAmount={investmentTransferAmount}
            investmentTransferDate={investmentTransferDate}
            investmentTransferNote={investmentTransferNote}
            onOpenInvestmentTransfer={openInvestmentTransfer}
            onCloseInvestmentTransfer={closeInvestmentTransfer}
            onSubmitInvestmentTransfer={handleInvestmentTransfer}
            setInvestmentTransferAccountId={setInvestmentTransferAccountId}
            setInvestmentTransferPortfolioId={setInvestmentTransferPortfolioId}
            setInvestmentTransferDirection={setInvestmentTransferDirection}
            setInvestmentTransferAmount={setInvestmentTransferAmount}
            setInvestmentTransferDate={setInvestmentTransferDate}
            setInvestmentTransferNote={setInvestmentTransferNote}
          />

          {expenseCategories.length > 0 && (
            <section className="bg-white border rounded-xl p-4 shadow-sm">
              <h2 className="font-semibold">Expense categories</h2>
              <ul className="mt-3 divide-y text-sm">
                {expenseCategories.map(([category, amount]) => <li key={category} className="py-2 flex justify-between gap-4"><span>{category}</span><span>{formatThb(amount)}</span></li>)}
              </ul>
            </section>
          )}

          <section className="bg-white border rounded-xl p-4 shadow-sm">
            <div className="flex items-center justify-between gap-3"><h2 className="font-semibold">Activity</h2><span className="text-xs text-gray-400">{summary.eventCount} event{summary.eventCount === 1 ? "" : "s"}</span></div>
            {summary.events.length === 0 ? <p className="text-sm text-gray-500 mt-3">No cash flow events in {formatMonthLabel(month)}. Income, Expenses, and Net Cash Flow are all ฿0.00.</p> : <ActivityList events={summary.events} />}
          </section>
        </>
      )}
    </div>
  );
}

function SummaryCard({ label, value, tone }: { label: string; value: string; tone: "positive" | "negative" | "neutral" }) {
  const toneClass = tone === "positive" ? "text-green-700" : tone === "negative" ? "text-red-700" : "text-gray-800";
  return <article className="bg-white border rounded-xl p-4 shadow-sm"><p className="text-sm text-gray-500">{label}</p><p className={`text-xl font-semibold mt-1 ${toneClass}`}>{value}</p></article>;
}

function CoverageSection({
  coverage, loading, accountsLoading, onRetry,
  targetSettings, targetLoading, targetLoadError, onRetryTarget,
  targetEditing, targetDraft, setTargetDraft, targetSaving, targetSaveError,
  onOpenTargetEdit, onCancelTargetEdit, onSubmitTargetEdit, onClearTarget,
}: {
  coverage: RecordedExpenseCoverageResult | null;
  loading: boolean;
  accountsLoading: boolean;
  onRetry: () => void;
  targetSettings: CashFlowSettings | null;
  targetLoading: boolean;
  targetLoadError: string;
  onRetryTarget: () => void;
  targetEditing: boolean;
  targetDraft: string;
  setTargetDraft: (value: string) => void;
  targetSaving: boolean;
  targetSaveError: string;
  onOpenTargetEdit: () => void;
  onCancelTargetEdit: () => void;
  onSubmitTargetEdit: (event: FormEvent) => void;
  onClearTarget: () => void;
}) {
  const recordedMonthLabels = coverage?.recordedMonths.map(formatMonthLabel) ?? [];
  const monthRangeLabel = recordedMonthLabels.length === 0
    ? ""
    : recordedMonthLabels.length === 1
      ? recordedMonthLabels[0]
      : `${recordedMonthLabels[0]} – ${recordedMonthLabels[recordedMonthLabels.length - 1]}`;
  // Disclosures accompany any state where account evidence resolved — including
  // INSUFFICIENT_EVIDENCE, where an unexplained ฿0.00 tracked cash balance is
  // exactly the figure that most needs the untracked-account caveat.
  const showDisclosures = coverage != null && coverage.trackedCash !== null;
  const gap = coverage ? computeCoverageGap(targetSettings?.target_coverage_months ?? null, coverage) : null;

  return (
    <section aria-label="Recorded expense coverage" className="bg-white border rounded-xl p-4 shadow-sm space-y-4">
      <div>
        <h2 className="font-semibold">Recorded expense coverage</h2>
        <p className="text-xs text-gray-500 mt-1">Not affected by the selected month.</p>
      </div>

      {accountsLoading && <p className="text-sm text-gray-400">Loading tracked cash balance…</p>}
      {!accountsLoading && loading && <p className="text-sm text-gray-400">Loading recorded monthly expense evidence…</p>}

      {!accountsLoading && !loading && coverage && (
        <>
          <div className="grid gap-3 sm:grid-cols-2">
            <div>
              <p className="text-xs uppercase tracking-wide text-gray-400">Current resource evidence</p>
              <p className="text-sm text-gray-600 mt-1">Tracked cash balance</p>
              {coverage.trackedCash !== null
                ? <p className="text-lg font-semibold mt-0.5">{formatThb(coverage.trackedCash)}</p>
                : <p className="text-sm text-gray-500 mt-0.5">Unavailable</p>}
            </div>
            <div>
              <p className="text-xs uppercase tracking-wide text-gray-400">Trailing historical evidence</p>
              <p className="text-sm text-gray-600 mt-1">Average recorded monthly expenses</p>
              {coverage.averageRecordedMonthlyExpense !== null
                ? <p className="text-lg font-semibold mt-0.5">{formatThb(coverage.averageRecordedMonthlyExpense)}</p>
                : <p className="text-sm text-gray-500 mt-0.5">{coverage.status === "INSUFFICIENT_EVIDENCE" ? "Not enough recorded history" : "Unavailable"}</p>}
              <p className="text-xs text-gray-500 mt-1">{coverage.recordedMonths.length} of 3 months recorded{monthRangeLabel ? ` (${monthRangeLabel})` : ""}</p>
            </div>
          </div>

          <p className="text-sm text-gray-800">
            {coverage.status === "AVAILABLE" && coverage.coverageMonths !== null &&
              `Tracked cash covers ${coverage.coverageMonths.toFixed(1)} months of average recorded monthly expenses (${monthRangeLabel}).`}
            {coverage.status === "NO_RECORDED_EXPENSE" &&
              `No recorded expenses in the recorded months (${monthRangeLabel}); recorded expense coverage cannot be expressed as a ratio.`}
            {coverage.status === "INSUFFICIENT_EVIDENCE" &&
              "Not enough recorded history yet to calculate recorded expense coverage."}
            {coverage.status === "UNAVAILABLE" && "Recorded expense coverage is unavailable right now."}
          </p>

          {coverage.status === "UNAVAILABLE" && (
            <button type="button" onClick={onRetry} className="text-sm text-blue-700 hover:underline">Try again</button>
          )}

          <div className="border-t pt-3 space-y-2">
            {targetLoading && <p className="text-xs text-gray-400">Loading your target…</p>}
            {!targetLoading && targetLoadError && (
              <div role="alert" className="text-xs text-red-600 space-y-1">
                <p>{targetLoadError}</p>
                <button type="button" onClick={onRetryTarget} className="text-blue-600 hover:underline">Try again</button>
              </div>
            )}
            {!targetLoading && !targetLoadError && !targetEditing && (
              <div className="flex items-center gap-3 flex-wrap">
                {targetSettings?.target_coverage_months == null ? (
                  <p className="text-sm text-gray-500">No target set.</p>
                ) : (
                  <p className="text-sm text-gray-800">
                    Your target: {targetSettings.target_coverage_months} months
                    {gap ? ` (${formatThb(gap.targetAmount)})` : ""}
                  </p>
                )}
                <button type="button" onClick={onOpenTargetEdit} className="text-xs text-blue-600 hover:underline">
                  {targetSettings?.target_coverage_months == null ? "Set target" : "Edit"}
                </button>
                {targetSettings?.target_coverage_months != null && (
                  <button type="button" onClick={onClearTarget} disabled={targetSaving} className="text-xs text-gray-500 hover:underline">Clear</button>
                )}
              </div>
            )}
            {!targetLoading && !targetLoadError && targetEditing && (
              <form onSubmit={onSubmitTargetEdit} className="flex items-center gap-2 flex-wrap">
                <label className="text-sm">
                  Target months
                  <input
                    aria-label="Target coverage months"
                    type="number"
                    min="0.1"
                    step="0.1"
                    value={targetDraft}
                    onChange={(event) => setTargetDraft(event.target.value)}
                    placeholder="Months"
                    className="ml-2 border rounded px-2 py-1 w-24"
                  />
                </label>
                <button type="submit" disabled={targetSaving} className="text-sm text-blue-600 hover:underline">Save</button>
                <button type="button" onClick={onCancelTargetEdit} className="text-sm text-gray-600">Cancel</button>
              </form>
            )}
            {targetSaveError && <p role="alert" className="text-xs text-red-600">{targetSaveError}</p>}
            {gap && !targetEditing && (
              <p className="text-sm text-gray-800">
                {gap.gapAmount < 0 && `${formatThb(Math.abs(gap.gapAmount))} more tracked cash would reach your target.`}
                {gap.gapAmount > 0 && `Tracked cash is ${formatThb(gap.gapAmount)} above your target.`}
                {gap.gapAmount === 0 && "Tracked cash matches your target."}
              </p>
            )}
          </div>

          {showDisclosures && (
            <ul className="text-xs text-gray-500 space-y-1 border-t pt-3">
              {coverage.untrackedActiveAccountCount > 0 && (
                <li>{coverage.untrackedActiveAccountCount} active cash account{coverage.untrackedActiveAccountCount === 1 ? "" : "s"} {coverage.untrackedActiveAccountCount === 1 ? "is" : "are"} not tracked and {coverage.untrackedActiveAccountCount === 1 ? "is" : "are"} not included.</li>
              )}
              {coverage.hasArchivedAccountExpenses && (
                <li>Recorded expenses include archived account(s) whose balances are not counted.</li>
              )}
              {coverage.accountsBeganDuringRecordedPeriod > 0 && (
                <li>Cash tracking for {coverage.accountsBeganDuringRecordedPeriod} account{coverage.accountsBeganDuringRecordedPeriod === 1 ? "" : "s"} began during this period.</li>
              )}
              <li>Amounts designated toward goals are not deducted here.</li>
            </ul>
          )}
        </>
      )}
    </section>
  );
}

function TemplatesSection({
  templates, loading, error, onRetry, trackedAccountIds, onUse,
  accounts, formOpen, editingId, name, type, accountId, amount, category, note, mutationError,
  onOpenCreate, onOpenEdit, onClose, onSubmit, onDelete,
  setName, setType, setAccountId, setAmount, setCategory, setNote,
}: {
  templates: CashEntryTemplate[] | null;
  loading: boolean;
  error: string;
  onRetry: () => void;
  trackedAccountIds: Set<number>;
  onUse: (template: CashEntryTemplate) => void;
  accounts: CashAccount[];
  formOpen: boolean;
  editingId: number | null;
  name: string;
  type: EntryType;
  accountId: string;
  amount: string;
  category: string;
  note: string;
  mutationError: string;
  onOpenCreate: () => void;
  onOpenEdit: (template: CashEntryTemplate) => void;
  onClose: () => void;
  onSubmit: (event: FormEvent) => void;
  onDelete: (id: number) => void;
  setName: (value: string) => void;
  setType: (value: EntryType) => void;
  setAccountId: (value: string) => void;
  setAmount: (value: string) => void;
  setCategory: (value: string) => void;
  setNote: (value: string) => void;
}) {
  const list = templates ?? [];
  const editingTemplate = editingId != null ? list.find((template) => template.id === editingId) ?? null : null;
  const editingArchivedAccount = editingTemplate?.cash_account_is_archived
    ? { name: editingTemplate.cash_account_name }
    : null;
  return (
    <section aria-label="Cash entry templates" className="bg-white border rounded-xl p-4 shadow-sm space-y-3">
      <div className="flex items-center justify-between gap-3">
        <div>
          <h2 className="font-semibold">Templates</h2>
          <p className="text-xs text-gray-500 mt-1">Prefill Add income / Add expense with saved defaults. You review and submit every entry yourself.</p>
        </div>
        {!formOpen && <button type="button" onClick={onOpenCreate} className="text-sm text-blue-600 hover:underline">Add template</button>}
      </div>

      {loading && <p className="text-sm text-gray-400">Loading templates…</p>}
      {!loading && error && (
        <div role="alert" className="text-sm text-red-600 space-y-1">
          <p>{error}</p>
          <button type="button" onClick={onRetry} className="text-blue-600 hover:underline">Try again</button>
        </div>
      )}

      {!loading && !error && list.length === 0 && !formOpen && (
        <p className="text-sm text-gray-500">No templates yet. Save one to skip re-entering the same Income or Expense fields.</p>
      )}

      {!loading && !error && list.length > 0 && (
        <ul className="divide-y text-sm">
          {list.map((template) => {
            const usable = trackedAccountIds.has(template.cash_account_id);
            const unusableReason = template.cash_account_is_archived ? "Account archived" : "Account not currently tracked";
            return (
              <li key={template.id} className="py-2 flex items-center justify-between gap-3">
                <div className="min-w-0">
                  <p className="font-medium truncate">{template.name}</p>
                  <p className="text-xs text-gray-500 mt-0.5">
                    {template.transaction_type === "INCOME" ? "Income" : "Expense"} · {template.category} · {formatTemplateAmount(template.amount)} · {template.cash_account_name ?? "Unknown account"}
                    {template.cash_account_is_archived && " (Archived)"}
                  </p>
                </div>
                <div className="flex items-center gap-2 shrink-0">
                  <button
                    type="button"
                    disabled={!usable}
                    onClick={() => onUse(template)}
                    title={usable ? undefined : unusableReason}
                    className="text-xs px-2 py-1 rounded border border-blue-600 text-blue-700 hover:bg-blue-50 disabled:opacity-40 disabled:cursor-not-allowed disabled:border-gray-300 disabled:text-gray-400"
                  >
                    {usable ? "Use template" : unusableReason}
                  </button>
                  <button type="button" onClick={() => onOpenEdit(template)} className="text-xs text-gray-600 hover:underline">Edit</button>
                  <button type="button" onClick={() => onDelete(template.id)} className="text-xs text-red-600 hover:underline">Delete</button>
                </div>
              </li>
            );
          })}
        </ul>
      )}

      {formOpen && (
        <form onSubmit={onSubmit} className="border-t pt-3 space-y-3">
          <h3 className="font-medium">{editingId != null ? "Edit template" : "Add template"}</h3>
          <div className="grid gap-3 sm:grid-cols-2">
            <label className="text-sm">Name
              <input aria-label="Template name" value={name} onChange={(event) => setName(event.target.value)} className={inputClass} />
            </label>
            <label className="text-sm">Type
              <select aria-label="Template type" value={type} onChange={(event) => setType(event.target.value as EntryType)} className={inputClass}>
                <option value="INCOME">Income</option>
                <option value="EXPENSE">Expense</option>
              </select>
            </label>
            <label className="text-sm">Cash account
              {editingArchivedAccount && (
                <p className="text-xs text-gray-600 mt-1 mb-1">
                  Current account: {editingArchivedAccount.name ?? "Unknown account"} — Archived
                </p>
              )}
              <select aria-label="Template cash account" value={accountId} onChange={(event) => setAccountId(event.target.value)} className={inputClass}>
                {editingArchivedAccount && <option value="">Keep current (archived) account</option>}
                {accounts.map((account) => <option key={account.id} value={account.id}>{account.name}</option>)}
              </select>
            </label>
            <label className="text-sm">Amount (THB)
              <input aria-label="Template amount" type="number" min="0.01" step="0.01" value={amount} onChange={(event) => setAmount(event.target.value)} className={inputClass} />
            </label>
            <label className="text-sm">Category
              <input aria-label="Template category" value={category} onChange={(event) => setCategory(event.target.value)} className={inputClass} />
            </label>
            <label className="text-sm sm:col-span-2">Note (optional)
              <input aria-label="Template note" value={note} onChange={(event) => setNote(event.target.value)} className={inputClass} />
            </label>
          </div>
          {mutationError && <p role="alert" className="text-sm text-red-600">{mutationError}</p>}
          <div className="flex gap-2">
            <button type="submit" className="bg-blue-600 text-white px-3 py-1.5 rounded text-sm hover:bg-blue-700">Save template</button>
            <button type="button" onClick={onClose} className="text-sm text-gray-600">Cancel</button>
          </div>
        </form>
      )}
    </section>
  );
}

function formatTemplateAmount(amount: number): string {
  return amount.toLocaleString("th-TH", { style: "currency", currency: "THB", minimumFractionDigits: 2 });
}

function TrendSection({
  trend, loading, accountsLoading, windowSize, onWindowSizeChange, onRetry,
}: {
  trend: CashFlowTrendResult | null;
  loading: boolean;
  accountsLoading: boolean;
  windowSize: TrendWindowSize;
  onWindowSizeChange: (size: TrendWindowSize) => void;
  onRetry: () => void;
}) {
  const allUnavailable = trend != null && trend.points.length > 0 && trend.points.every((point) => point.status === "UNAVAILABLE");

  return (
    <section aria-label="Cash flow trend" className="bg-white border rounded-xl p-4 shadow-sm space-y-3">
      <div className="flex items-center justify-between gap-3 flex-wrap">
        <div>
          <h2 className="font-semibold">Cash Flow Trend</h2>
          <p className="text-xs text-gray-500 mt-1">Historical monthly Income, Expenses, and Net Cash Flow. Completed months only — not a forecast.</p>
        </div>
        <div className="flex items-center gap-0.5">
          {TREND_WINDOW_SIZES.map((size) => (
            <button
              key={size}
              type="button"
              onClick={() => onWindowSizeChange(size)}
              className={`text-xs px-2.5 py-1 rounded-md font-medium transition-colors ${
                size === windowSize ? "bg-blue-600 text-white" : "text-gray-500 hover:bg-gray-100"
              }`}
            >
              {size}M
            </button>
          ))}
        </div>
      </div>

      {(accountsLoading || loading) && <p className="text-sm text-gray-400">Loading Cash Flow Trend…</p>}

      {!accountsLoading && !loading && trend && (
        allUnavailable ? (
          <div role="alert" className="border border-red-200 bg-red-50 rounded-xl p-4 text-sm text-red-700 space-y-2">
            <p>Unable to load Cash Flow Trend.</p>
            <button type="button" onClick={onRetry} className="text-blue-700 hover:underline">Try again</button>
          </div>
        ) : (
          <>
            <CashFlowTrendChart points={trend.points} />
            {trend.summary.availableMonths > 0 && (
              <div className="grid gap-3 sm:grid-cols-4 text-sm border-t pt-3">
                <TrendSummaryStat label="Avg Income" value={trend.summary.averageIncome} />
                <TrendSummaryStat label="Avg Expenses" value={trend.summary.averageExpenses} />
                <TrendSummaryStat label="Avg Net Cash Flow" value={trend.summary.averageNetCashFlow} />
                <TrendSummaryStat label="Latest Net Cash Flow" value={trend.summary.latestAvailableNetCashFlow} />
              </div>
            )}
            <p className="text-xs text-gray-500">{`${trend.summary.availableMonths} of ${trend.summary.requestedMonths} months available.`}</p>
          </>
        )
      )}
    </section>
  );
}

function TrendSummaryStat({ label, value }: { label: string; value: number | null }) {
  return (
    <div>
      <p className="text-xs uppercase tracking-wide text-gray-400">{label}</p>
      <p className="text-sm font-semibold mt-0.5">{value !== null ? formatThb(value) : "—"}</p>
    </div>
  );
}

function EntrySection({
  accounts, accountsLoading, accountsError, onRetryAccounts, entryType, entryAccountId, entryAmount,
  entryDate, entryCategory, entryNote, mutationError, onOpen, onClose, onSubmit, setEntryAccountId,
  setEntryAmount, setEntryDate, setEntryCategory, setEntryNote,
  transferOpen, transferSourceId, transferDestinationId, transferAmount, transferDate, transferNote,
  onOpenTransfer, onCloseTransfer, onSubmitTransfer, setTransferSourceId, setTransferDestinationId,
  setTransferAmount, setTransferDate, setTransferNote,
  portfolios, portfoliosLoading, investmentTransferOpen, investmentTransferAccountId, investmentTransferPortfolioId,
  investmentTransferDirection, investmentTransferAmount, investmentTransferDate, investmentTransferNote,
  onOpenInvestmentTransfer, onCloseInvestmentTransfer, onSubmitInvestmentTransfer,
  setInvestmentTransferAccountId, setInvestmentTransferPortfolioId, setInvestmentTransferDirection,
  setInvestmentTransferAmount, setInvestmentTransferDate, setInvestmentTransferNote,
}: {
  accounts: CashAccount[];
  accountsLoading: boolean;
  accountsError: string;
  onRetryAccounts: () => void;
  entryType: EntryType | null;
  entryAccountId: string;
  entryAmount: string;
  entryDate: string;
  entryCategory: string;
  entryNote: string;
  mutationError: string;
  onOpen: (type: EntryType) => void;
  onClose: () => void;
  onSubmit: (event: FormEvent) => void;
  setEntryAccountId: (value: string) => void;
  setEntryAmount: (value: string) => void;
  setEntryDate: (value: string) => void;
  setEntryCategory: (value: string) => void;
  setEntryNote: (value: string) => void;
  transferOpen: boolean;
  transferSourceId: string;
  transferDestinationId: string;
  transferAmount: string;
  transferDate: string;
  transferNote: string;
  onOpenTransfer: () => void;
  onCloseTransfer: () => void;
  onSubmitTransfer: (event: FormEvent) => void;
  setTransferSourceId: (value: string) => void;
  setTransferDestinationId: (value: string) => void;
  setTransferAmount: (value: string) => void;
  setTransferDate: (value: string) => void;
  setTransferNote: (value: string) => void;
  portfolios: Portfolio[];
  portfoliosLoading: boolean;
  investmentTransferOpen: boolean;
  investmentTransferAccountId: string;
  investmentTransferPortfolioId: string;
  investmentTransferDirection: "TO_PORTFOLIO" | "FROM_PORTFOLIO";
  investmentTransferAmount: string;
  investmentTransferDate: string;
  investmentTransferNote: string;
  onOpenInvestmentTransfer: () => void;
  onCloseInvestmentTransfer: () => void;
  onSubmitInvestmentTransfer: (event: FormEvent) => void;
  setInvestmentTransferAccountId: (value: string) => void;
  setInvestmentTransferPortfolioId: (value: string) => void;
  setInvestmentTransferDirection: (value: "TO_PORTFOLIO" | "FROM_PORTFOLIO") => void;
  setInvestmentTransferAmount: (value: string) => void;
  setInvestmentTransferDate: (value: string) => void;
  setInvestmentTransferNote: (value: string) => void;
}) {
  const source = accounts.find((account) => account.id === Number(transferSourceId));
  const destination = accounts.find((account) => account.id === Number(transferDestinationId));
  const transferAmountValue = Number(transferAmount);
  const investmentTransferAccount = accounts.find((account) => account.id === Number(investmentTransferAccountId));
  const investmentTransferPortfolio = portfolios.find((portfolio) => portfolio.id === Number(investmentTransferPortfolioId));
  const investmentTransferAmountValue = Number(investmentTransferAmount);
  const canOpenInvestmentTransfer = accounts.length > 0 && portfolios.length > 0;
  return (
    <section className="bg-white border rounded-xl p-4 shadow-sm space-y-3">
      <div><h2 className="font-semibold">Add activity</h2><p className="text-xs text-gray-500 mt-1">Only active accounts with explicit Cash Flow tracking can receive new events.</p></div>
      {accountsLoading && <p className="text-sm text-gray-400">Loading tracked accounts…</p>}
      {!accountsLoading && accountsError && <div role="alert" className="text-sm text-red-600 space-y-1"><p>{accountsError}</p><button type="button" onClick={onRetryAccounts} className="text-blue-600 hover:underline">Try again</button></div>}
      {!accountsLoading && !accountsError && accounts.length === 0 && <p className="text-sm text-gray-500">No active tracked cash account is available. Transfers need two active tracked accounts. <Link href="/cash" className="text-blue-600 hover:underline">Start tracking under Cash Accounts →</Link></p>}
      {!accountsLoading && !accountsError && accounts.length > 0 && !entryType && !transferOpen && !investmentTransferOpen && <div className="flex gap-3 flex-wrap"><button type="button" onClick={() => onOpen("INCOME")} className="bg-blue-600 text-white px-3 py-1.5 rounded text-sm hover:bg-blue-700">Add income</button><button type="button" onClick={() => onOpen("EXPENSE")} className="border border-blue-600 text-blue-700 px-3 py-1.5 rounded text-sm hover:bg-blue-50">Add expense</button>{accounts.length >= 2 && <button type="button" onClick={onOpenTransfer} className="border border-gray-500 text-gray-700 px-3 py-1.5 rounded text-sm hover:bg-gray-50">Transfer</button>}{!portfoliosLoading && canOpenInvestmentTransfer && <button type="button" onClick={onOpenInvestmentTransfer} className="border border-gray-500 text-gray-700 px-3 py-1.5 rounded text-sm hover:bg-gray-50">Investment transfer</button>}</div>}
      {!accountsLoading && !accountsError && accounts.length === 1 && !entryType && !transferOpen && <p className="text-xs text-gray-500">Transfer requires at least two active tracked Cash Accounts. <Link href="/cash" className="text-blue-600 hover:underline">Add or start tracking another account →</Link></p>}
      {entryType && <form onSubmit={onSubmit} className="border-t pt-3 space-y-3"><h3 className="font-medium">Add {entryType === "INCOME" ? "income" : "expense"}</h3><div className="grid gap-3 sm:grid-cols-2"><label className="text-sm">Cash account<select aria-label="Cash flow account" value={entryAccountId} onChange={(event) => setEntryAccountId(event.target.value)} className={inputClass}>{accounts.map((account) => <option key={account.id} value={account.id}>{account.name}</option>)}</select></label><label className="text-sm">Amount (THB)<input aria-label="Cash flow amount" type="number" min="0.01" step="0.01" value={entryAmount} onChange={(event) => setEntryAmount(event.target.value)} className={inputClass} /></label><label className="text-sm">Occurred date<input aria-label="Cash flow date" type="date" value={entryDate} onChange={(event) => setEntryDate(event.target.value)} className={inputClass} /></label><label className="text-sm">Category<input aria-label="Cash flow category" value={entryCategory} onChange={(event) => setEntryCategory(event.target.value)} className={inputClass} /></label><label className="text-sm sm:col-span-2">Note (optional)<input aria-label="Cash flow note" value={entryNote} onChange={(event) => setEntryNote(event.target.value)} className={inputClass} /></label></div>{mutationError && <p role="alert" className="text-sm text-red-600">{mutationError}</p>}<div className="flex gap-2"><button type="submit" className="bg-blue-600 text-white px-3 py-1.5 rounded text-sm hover:bg-blue-700">Save {entryType === "INCOME" ? "income" : "expense"}</button><button type="button" onClick={onClose} className="text-sm text-gray-600">Cancel</button></div></form>}
      {transferOpen && <form onSubmit={onSubmitTransfer} className="border-t pt-3 space-y-3"><h3 className="font-medium">Transfer between Cash Accounts</h3><div className="grid gap-3 sm:grid-cols-2"><label className="text-sm">From Account<select aria-label="Transfer from account" value={transferSourceId} onChange={(event) => { setTransferSourceId(event.target.value); if (event.target.value === transferDestinationId) setTransferDestinationId(String(accounts.find((account) => account.id !== Number(event.target.value))?.id ?? "")); }} className={inputClass}>{accounts.map((account) => <option key={account.id} value={account.id}>{account.name}</option>)}</select></label><label className="text-sm">To Account<select aria-label="Transfer to account" value={transferDestinationId} onChange={(event) => setTransferDestinationId(event.target.value)} className={inputClass}>{accounts.filter((account) => account.id !== Number(transferSourceId)).map((account) => <option key={account.id} value={account.id}>{account.name}</option>)}</select></label><label className="text-sm">Amount (THB)<input aria-label="Transfer amount" type="number" min="0.01" step="0.01" value={transferAmount} onChange={(event) => setTransferAmount(event.target.value)} className={inputClass} /></label><label className="text-sm">Occurred date<input aria-label="Transfer date" type="date" value={transferDate} onChange={(event) => setTransferDate(event.target.value)} className={inputClass} /></label><label className="text-sm sm:col-span-2">Note (optional)<input aria-label="Transfer note" value={transferNote} onChange={(event) => setTransferNote(event.target.value)} className={inputClass} /></label></div><p className="text-sm text-gray-700">Transfer preview: <strong>{source?.name ?? "—"} → {destination?.name ?? "—"}</strong>{Number.isFinite(transferAmountValue) && transferAmountValue > 0 ? ` · ${formatThb(transferAmountValue)}` : ""}</p>{mutationError && <p role="alert" className="text-sm text-red-600">{mutationError}</p>}<div className="flex gap-2"><button type="submit" className="bg-gray-700 text-white px-3 py-1.5 rounded text-sm hover:bg-gray-800">Save transfer</button><button type="button" onClick={onCloseTransfer} className="text-sm text-gray-600">Cancel</button></div></form>}
      {investmentTransferOpen && (
        <form onSubmit={onSubmitInvestmentTransfer} className="border-t pt-3 space-y-3">
          <h3 className="font-medium">Record investment transfer</h3>
          <div className="grid gap-3 sm:grid-cols-2">
            <label className="text-sm">Direction
              <select aria-label="Investment transfer direction" value={investmentTransferDirection} onChange={(event) => setInvestmentTransferDirection(event.target.value as "TO_PORTFOLIO" | "FROM_PORTFOLIO")} className={inputClass}>
                <option value="TO_PORTFOLIO">Cash → Investment</option>
                <option value="FROM_PORTFOLIO">Investment → Cash</option>
              </select>
            </label>
            <label className="text-sm">Cash account
              <select aria-label="Investment transfer cash account" value={investmentTransferAccountId} onChange={(event) => setInvestmentTransferAccountId(event.target.value)} className={inputClass}>
                {accounts.map((account) => <option key={account.id} value={account.id}>{account.name}</option>)}
              </select>
            </label>
            <label className="text-sm">Investment portfolio
              <select aria-label="Investment transfer portfolio" value={investmentTransferPortfolioId} onChange={(event) => setInvestmentTransferPortfolioId(event.target.value)} className={inputClass}>
                {portfolios.map((portfolio) => <option key={portfolio.id} value={portfolio.id}>{portfolio.name}</option>)}
              </select>
            </label>
            <label className="text-sm">Amount (THB)
              <input aria-label="Investment transfer amount" type="number" min="0.01" step="0.01" value={investmentTransferAmount} onChange={(event) => setInvestmentTransferAmount(event.target.value)} className={inputClass} />
            </label>
            <label className="text-sm">Date
              <input aria-label="Investment transfer date" type="date" value={investmentTransferDate} onChange={(event) => setInvestmentTransferDate(event.target.value)} className={inputClass} />
            </label>
            <label className="text-sm sm:col-span-2">Note (optional)
              <input aria-label="Investment transfer note" value={investmentTransferNote} onChange={(event) => setInvestmentTransferNote(event.target.value)} className={inputClass} />
            </label>
          </div>
          <p className="text-sm text-gray-700">
            {investmentTransferDirection === "TO_PORTFOLIO"
              ? <>{investmentTransferAccount?.name ?? "—"} → {investmentTransferPortfolio?.name ?? "—"}</>
              : <>{investmentTransferPortfolio?.name ?? "—"} → {investmentTransferAccount?.name ?? "—"}</>}
            {Number.isFinite(investmentTransferAmountValue) && investmentTransferAmountValue > 0 ? ` · ${formatThb(investmentTransferAmountValue)}` : ""}
          </p>
          <p className="text-xs text-gray-500">Records the cash side only. The portfolio&apos;s deposit or withdrawal is recorded separately in the investment ledger.</p>
          {mutationError && <p role="alert" className="text-sm text-red-600">{mutationError}</p>}
          <div className="flex gap-2">
            <button type="submit" className="bg-gray-700 text-white px-3 py-1.5 rounded text-sm hover:bg-gray-800">Record transfer</button>
            <button type="button" onClick={onCloseInvestmentTransfer} className="text-sm text-gray-600">Cancel</button>
          </div>
        </form>
      )}
    </section>
  );
}

function ActivityList({ events }: { events: CashFlowEvent[] }) {
  return <ul className="mt-3 divide-y">{events.map((event) => <li key={event.transfer_id ? `transfer-${event.transfer_id}` : `transaction-${event.id}`} className="py-3 flex items-start justify-between gap-4"><div className="min-w-0"><p className="text-sm font-medium">{event.occurred_on} · {eventActivityLabel(event)}</p><p className="text-xs text-gray-500 mt-0.5">{eventTypeLabel(event)}{event.category ? ` · ${event.category}` : ""}</p>{investmentTransferEvidence(event)}{event.note && <p className="text-xs text-gray-600 mt-1 break-words">{event.note}</p>}</div><span className={`text-sm font-medium whitespace-nowrap ${event.transaction_type === "TRANSFER" ? "text-gray-700" : signedPresentationAmount(event) >= 0 ? "text-green-700" : "text-red-700"}`}>{event.transaction_type === "TRANSFER" ? formatThb(event.amount) : formatSigned(signedPresentationAmount(event))}</span></li>)}</ul>;
}

function eventTypeLabel(event: CashFlowEvent): string {
  if (event.transaction_type === "INCOME") return "Income";
  if (event.transaction_type === "EXPENSE") return "Expense";
  if (event.transaction_type === "TRANSFER") return "Transfer";
  if (event.transaction_type === "INVESTMENT_TRANSFER") return "Investment transfer";
  return "Adjustment";
}

function eventActivityLabel(event: CashFlowEvent): string {
  if (event.transaction_type === "TRANSFER") {
    const source = `${event.transfer_source_account_name ?? event.account_name}${event.source_account_is_archived ? " (Archived)" : ""}`;
    const destination = `${event.transfer_destination_account_name ?? "destination"}${event.destination_account_is_archived ? " (Archived)" : ""}`;
    return `${source} → ${destination}`;
  }
  if (event.transaction_type === "INVESTMENT_TRANSFER") {
    const account = `${event.account_name}${event.account_is_archived ? " (Archived)" : ""}`;
    const portfolio = event.counterparty_portfolio_name ?? "Investment portfolio (no longer available)";
    return event.investment_direction === "FROM_PORTFOLIO" ? `${portfolio} → ${account}` : `${account} → ${portfolio}`;
  }
  return `${event.account_name}${event.account_is_archived ? " (Archived)" : ""}`;
}

function investmentTransferEvidence(event: CashFlowEvent) {
  if (event.transaction_type !== "INVESTMENT_TRANSFER") return null;
  if (event.counterparty_portfolio_id != null) {
    const name = event.counterparty_portfolio_name ?? "Associated portfolio";
    return <p className="text-xs text-gray-500 mt-0.5">Associated portfolio: <Link href={`/portfolio?portfolio=${event.counterparty_portfolio_id}`} className="text-blue-600 hover:underline">{name}</Link></p>;
  }
  if (event.counterparty_portfolio_name_snapshot) {
    return <p className="text-xs text-gray-500 mt-0.5">Historical associated portfolio: {event.counterparty_portfolio_name_snapshot} (no longer available)</p>;
  }
  return <p className="text-xs text-gray-500 mt-0.5">Associated portfolio is no longer available; no historical portfolio identity was recorded.</p>;
}

function formatSigned(value: number): string {
  return `${value >= 0 ? "+" : "−"}${formatThb(Math.abs(value))}`;
}
