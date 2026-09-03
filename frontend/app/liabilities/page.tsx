"use client";

import { FormEvent, useEffect, useRef, useState } from "react";
import {
  createLiability,
  createLiabilityBalanceObservation,
  getLiabilityBalanceAsOf,
  listLiabilities,
  listLiabilityBalanceObservations,
  updateLiability,
  type Liability,
  type LiabilityBalanceAsOf,
  type LiabilityBalanceObservation,
  type LiabilityType,
} from "@/lib/api";

const LIABILITY_TYPES: LiabilityType[] = [
  "MORTGAGE",
  "AUTO_LOAN",
  "PERSONAL_LOAN",
  "CREDIT_CARD",
  "STUDENT_LOAN",
  "OTHER",
];

const typeLabel = (value: LiabilityType) => ({
  MORTGAGE: "Mortgage",
  AUTO_LOAN: "Auto loan",
  PERSONAL_LOAN: "Personal loan",
  CREDIT_CARD: "Credit card",
  STUDENT_LOAN: "Student loan",
  OTHER: "Other",
}[value]);

const formatThb = (value: number) => value.toLocaleString("th-TH", {
  style: "currency",
  currency: "THB",
  minimumFractionDigits: 2,
});
const messageFor = (error: unknown, fallback: string) => error instanceof Error ? error.message : fallback;
const inputClass = "mt-1 block w-full border rounded px-3 py-2";
const today = () => new Date().toISOString().slice(0, 10);

export default function LiabilitiesPage() {
  const [liabilities, setLiabilities] = useState<Liability[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [mutationError, setMutationError] = useState("");
  const [showArchived, setShowArchived] = useState(false);

  const [name, setName] = useState("");
  const [liabilityType, setLiabilityType] = useState<LiabilityType>("OTHER");
  const [lender, setLender] = useState("");
  const [balance, setBalance] = useState("");
  const [note, setNote] = useState("");

  const [editing, setEditing] = useState<Liability | null>(null);
  const [editName, setEditName] = useState("");
  const [editType, setEditType] = useState<LiabilityType>("OTHER");
  const [editLender, setEditLender] = useState("");
  const [editNote, setEditNote] = useState("");
  const [balanceTarget, setBalanceTarget] = useState<Liability | null>(null);
  const [replacementBalance, setReplacementBalance] = useState("");
  const [recordTarget, setRecordTarget] = useState<Liability | null>(null);
  const [recordDate, setRecordDate] = useState(today());
  const [recordBalance, setRecordBalance] = useState("");

  const [historyTarget, setHistoryTarget] = useState<Liability | null>(null);
  const [historyRows, setHistoryRows] = useState<LiabilityBalanceObservation[]>([]);
  const [historyLoading, setHistoryLoading] = useState(false);
  const [historyError, setHistoryError] = useState("");
  const historyRequestId = useRef(0);

  const [asOfTarget, setAsOfTarget] = useState<Liability | null>(null);
  const [asOfDate, setAsOfDate] = useState(today());
  const [asOfResult, setAsOfResult] = useState<LiabilityBalanceAsOf | null>(null);
  const [asOfLoading, setAsOfLoading] = useState(false);
  const [asOfError, setAsOfError] = useState("");
  const asOfRequestId = useRef(0);

  async function load(includeArchived = showArchived) {
    setLoading(true);
    setError("");
    try {
      setLiabilities(await listLiabilities(includeArchived));
    } catch (err) {
      setLiabilities([]);
      setError(messageFor(err, "Unable to load liabilities."));
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

  async function handleCreate(event: FormEvent) {
    event.preventDefault();
    setMutationError("");
    const parsed = Number(balance);
    if (!name.trim() || !balance.trim() || !Number.isFinite(parsed) || parsed < 0) {
      setMutationError("Enter a liability name and a non-negative observed balance.");
      return;
    }
    try {
      await createLiability({
        name: name.trim(),
        liability_type: liabilityType,
        lender: lender.trim() || null,
        balance: parsed,
        currency: "THB",
        note: note.trim() || null,
      });
      setName("");
      setLiabilityType("OTHER");
      setLender("");
      setBalance("");
      setNote("");
      await load();
    } catch (err) {
      setMutationError(messageFor(err, "Unable to create liability."));
    }
  }

  function closeMutationForms() {
    setEditing(null);
    setBalanceTarget(null);
    setRecordTarget(null);
  }

  function openEdit(item: Liability) {
    setMutationError("");
    closeMutationForms();
    setEditing(item);
    setEditName(item.name);
    setEditType(item.liability_type);
    setEditLender(item.lender ?? "");
    setEditNote(item.note ?? "");
  }

  async function handleEdit(event: FormEvent) {
    event.preventDefault();
    if (!editing) return;
    setMutationError("");
    if (!editName.trim()) {
      setMutationError("Liability name cannot be blank.");
      return;
    }
    try {
      await updateLiability(editing.id, {
        name: editName.trim(),
        liability_type: editType,
        lender: editLender.trim() || null,
        note: editNote.trim() || null,
      });
      setEditing(null);
      await load();
    } catch (err) {
      setMutationError(messageFor(err, "Unable to update liability."));
    }
  }

  function openBalanceUpdate(item: Liability) {
    setMutationError("");
    closeMutationForms();
    setBalanceTarget(item);
    setReplacementBalance(String(item.balance));
  }

  async function handleBalanceUpdate(event: FormEvent) {
    event.preventDefault();
    if (!balanceTarget) return;
    setMutationError("");
    const parsed = Number(replacementBalance);
    if (!replacementBalance.trim() || !Number.isFinite(parsed) || parsed < 0) {
      setMutationError("Enter a non-negative observed balance.");
      return;
    }
    try {
      await updateLiability(balanceTarget.id, { balance: parsed });
      setBalanceTarget(null);
      await load();
    } catch (err) {
      setMutationError(messageFor(err, "Unable to update liability balance."));
    }
  }

  function openRecord(item: Liability) {
    setMutationError("");
    closeMutationForms();
    setRecordTarget(item);
    setRecordDate(today());
    setRecordBalance(String(item.balance));
  }

  async function fetchHistory(liabilityId: number) {
    setHistoryError("");
    setHistoryLoading(true);
    const requestId = ++historyRequestId.current;
    try {
      const rows = await listLiabilityBalanceObservations(liabilityId);
      if (historyRequestId.current === requestId) setHistoryRows(rows);
    } catch (err) {
      if (historyRequestId.current === requestId) setHistoryError(messageFor(err, "Unable to load balance history."));
    } finally {
      if (historyRequestId.current === requestId) setHistoryLoading(false);
    }
  }

  function toggleHistory(item: Liability) {
    if (historyTarget?.id === item.id) {
      setHistoryTarget(null);
      return;
    }
    setMutationError("");
    closeAsOf();
    setHistoryTarget(item);
    setHistoryRows([]);
    void fetchHistory(item.id);
  }

  function closeAsOf() {
    // Invalidate any in-flight lookup so a late response can never populate a
    // different (or now-closed) target's panel.
    asOfRequestId.current += 1;
    setAsOfTarget(null);
    setAsOfResult(null);
    setAsOfError("");
    setAsOfLoading(false);
  }

  function openAsOf(item: Liability) {
    setMutationError("");
    setHistoryTarget(null);
    closeAsOf();
    setAsOfTarget(item);
    setAsOfDate(today());
  }

  async function handleAsOfLookup(event: FormEvent) {
    event.preventDefault();
    if (!asOfTarget) return;
    if (!asOfDate.trim()) {
      setAsOfError("Enter a date to look up.");
      return;
    }
    setAsOfError("");
    setAsOfLoading(true);
    const requestId = ++asOfRequestId.current;
    const liabilityId = asOfTarget.id;
    try {
      const result = await getLiabilityBalanceAsOf(liabilityId, asOfDate);
      if (asOfRequestId.current === requestId) setAsOfResult(result);
    } catch (err) {
      if (asOfRequestId.current === requestId) setAsOfError(messageFor(err, "Unable to look up historical balance."));
    } finally {
      if (asOfRequestId.current === requestId) setAsOfLoading(false);
    }
  }

  async function handleRecord(event: FormEvent) {
    event.preventDefault();
    if (!recordTarget) return;
    setMutationError("");
    const parsed = Number(recordBalance);
    if (!recordDate.trim() || !recordBalance.trim() || !Number.isFinite(parsed) || parsed < 0) {
      setMutationError("Enter a date and a non-negative observed balance.");
      return;
    }
    try {
      const recordedLiabilityId = recordTarget.id;
      await createLiabilityBalanceObservation(recordedLiabilityId, { balance: parsed, observed_on: recordDate });
      setRecordTarget(null);
      await load();
      if (historyTarget?.id === recordedLiabilityId) await fetchHistory(recordedLiabilityId);
    } catch (err) {
      setMutationError(messageFor(err, "Unable to record balance history."));
    }
  }

  async function setArchived(item: Liability, isArchived: boolean) {
    setMutationError("");
    try {
      await updateLiability(item.id, { is_archived: isArchived });
      await load();
    } catch (err) {
      setMutationError(messageFor(err, isArchived ? "Unable to archive liability." : "Unable to restore liability."));
    }
  }

  async function toggleArchived() {
    const next = !showArchived;
    setShowArchived(next);
    await load(next);
  }

  const active = liabilities.filter((item) => !item.is_archived);
  const archived = liabilities.filter((item) => item.is_archived);
  const activeValuesValid = active.every((item) => item.currency === "THB" && Number.isFinite(item.balance) && item.balance >= 0);
  const computedOutstanding = activeValuesValid ? active.reduce((total, item) => total + item.balance, 0) : null;
  const totalOutstanding = !loading && !error && computedOutstanding != null && Number.isFinite(computedOutstanding)
    ? computedOutstanding
    : null;

  return (
    <div className="space-y-6 max-w-3xl">
      <div>
        <h1 className="text-2xl font-bold">Liabilities</h1>
        <p className="text-sm text-gray-500 mt-1">Track current observed amounts owed. Updating a balance does not record a payment.</p>
      </div>

      <form onSubmit={handleCreate} className="bg-white border rounded-xl p-4 space-y-3 shadow-sm">
        <h2 className="font-semibold">Add liability</h2>
        <div className="grid gap-3 sm:grid-cols-2">
          <Field label="Name"><input aria-label="Liability name" value={name} onChange={(event) => setName(event.target.value)} className={inputClass} /></Field>
          <Field label="Type"><TypeSelect ariaLabel="Liability type" value={liabilityType} onChange={setLiabilityType} /></Field>
          <Field label="Lender (optional)"><input aria-label="Lender" value={lender} onChange={(event) => setLender(event.target.value)} className={inputClass} /></Field>
          <Field label="Current observed balance"><input aria-label="Initial balance" type="number" step="0.01" value={balance} onChange={(event) => setBalance(event.target.value)} className={inputClass} /></Field>
          <Field label="Note (optional)"><input aria-label="Note" value={note} onChange={(event) => setNote(event.target.value)} className={inputClass} /></Field>
        </div>
        <p className="text-xs text-gray-500">Currency: <strong>THB</strong> (fixed for Liability Foundation v1)</p>
        <PrimaryButton>Add liability</PrimaryButton>
      </form>

      {mutationError && <p role="alert" className="text-sm text-red-600">{mutationError}</p>}

      {editing && (
        <form onSubmit={handleEdit} className="bg-blue-50 border border-blue-200 rounded-xl p-4 space-y-3">
          <h2 className="font-semibold">Edit {editing.name}</h2>
          <div className="grid gap-3 sm:grid-cols-2">
            <Field label="Name"><input aria-label="Edit liability name" value={editName} onChange={(event) => setEditName(event.target.value)} className={inputClass} /></Field>
            <Field label="Type"><TypeSelect ariaLabel="Edit liability type" value={editType} onChange={setEditType} /></Field>
            <Field label="Lender"><input aria-label="Edit lender" value={editLender} onChange={(event) => setEditLender(event.target.value)} className={inputClass} /></Field>
            <Field label="Note"><input aria-label="Edit note" value={editNote} onChange={(event) => setEditNote(event.target.value)} className={inputClass} /></Field>
          </div>
          <Actions><PrimaryButton>Save changes</PrimaryButton><Cancel onClick={() => setEditing(null)} /></Actions>
        </form>
      )}

      {balanceTarget && (
        <form onSubmit={handleBalanceUpdate} className="bg-blue-50 border border-blue-200 rounded-xl p-4 space-y-3">
          <h2 className="font-semibold">Update balance — {balanceTarget.name}</h2>
          <p className="text-sm text-gray-600">Replace the current observed outstanding balance in THB. This does not create a payment or cash-flow event.</p>
          <Field label="Current observed balance (THB)"><input aria-label="Observed balance" type="number" step="0.01" value={replacementBalance} onChange={(event) => setReplacementBalance(event.target.value)} className={`${inputClass} max-w-xs`} /></Field>
          <Actions><PrimaryButton>Save balance</PrimaryButton><Cancel onClick={() => setBalanceTarget(null)} /></Actions>
        </form>
      )}

      {recordTarget && (
        <form onSubmit={handleRecord} className="bg-blue-50 border border-blue-200 rounded-xl p-4 space-y-3">
          <h2 className="font-semibold">Record balance — {recordTarget.name}</h2>
          <p className="text-sm text-gray-600">Record a dated observed balance. Earlier history is not reconstructed — only explicit dated observations become available for lookup.</p>
          <div className="grid gap-3 sm:grid-cols-2 max-w-md">
            <Field label="Observed date"><input aria-label="Observed date" type="date" value={recordDate} onChange={(event) => setRecordDate(event.target.value)} className={inputClass} /></Field>
            <Field label="Observed balance (THB)"><input aria-label="Observed balance on date" type="number" step="0.01" value={recordBalance} onChange={(event) => setRecordBalance(event.target.value)} className={inputClass} /></Field>
          </div>
          <Actions><PrimaryButton>Record balance</PrimaryButton><Cancel onClick={() => setRecordTarget(null)} /></Actions>
        </form>
      )}

      {historyTarget && (
        <div className="bg-gray-50 border rounded-xl p-4 space-y-3">
          <div className="flex items-center justify-between gap-3">
            <h2 className="font-semibold">Balance history — {historyTarget.name}</h2>
            <button type="button" onClick={() => setHistoryTarget(null)} className="text-sm text-gray-600">Close</button>
          </div>
          {historyLoading ? (
            <p className="text-sm text-gray-400">Loading balance history…</p>
          ) : historyError ? (
            <div className="text-sm text-red-600 space-y-2">
              <p role="alert">{historyError}</p>
              <button type="button" onClick={() => void fetchHistory(historyTarget.id)} className="text-blue-600 hover:underline">Try again</button>
            </div>
          ) : historyRows.length === 0 ? (
            <p className="text-sm text-gray-500">No recorded balance observations yet.</p>
          ) : (
            <ul className="space-y-1 text-sm">
              {historyRows.map((row) => (
                <li key={row.id} className="flex justify-between gap-3">
                  <span>Observed on {row.observed_on}</span>
                  <span className="font-medium">{formatThb(row.balance)}</span>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}

      {asOfTarget && (
        <form onSubmit={handleAsOfLookup} className="bg-gray-50 border rounded-xl p-4 space-y-3">
          <h2 className="font-semibold">Historical balance — {asOfTarget.name}</h2>
          <p className="text-sm text-gray-600">Look up the recorded/effective balance as of a prior date.</p>
          <Field label="Date"><input aria-label="As-of date" type="date" value={asOfDate} onChange={(event) => { setAsOfDate(event.target.value); setAsOfResult(null); setAsOfError(""); }} className={`${inputClass} max-w-xs`} /></Field>
          <Actions><PrimaryButton>{asOfLoading ? "Looking up…" : "Look up"}</PrimaryButton><Cancel onClick={closeAsOf} /></Actions>
          {asOfError && <p role="alert" className="text-sm text-red-600">{asOfError}</p>}
          {asOfResult && (
            asOfResult.available && asOfResult.balance != null ? (
              <p className="text-sm mt-2"><span className="font-medium">{formatThb(asOfResult.balance)}</span> <span className="text-xs text-gray-500">THB as of {asOfResult.date}</span></p>
            ) : (
              <p className="text-sm mt-2 text-gray-600">No recorded liability balance is available for this date.</p>
            )
          )}
        </form>
      )}

      <section className="space-y-3">
        <div className="flex items-center justify-between gap-3 flex-wrap">
          <div>
            <h2 className="text-lg font-semibold">Active liabilities</h2>
            <p className="text-sm text-gray-500">Total Outstanding: <strong>{error ? "Unavailable" : loading ? "Loading…" : totalOutstanding == null ? "Unavailable" : formatThb(totalOutstanding)}</strong></p>
          </div>
          <button type="button" onClick={() => void toggleArchived()} className="text-sm text-blue-600 hover:underline">{showArchived ? "Hide archived" : "Show archived"}</button>
        </div>
        {loading ? <p className="text-sm text-gray-400">Loading liabilities…</p> : error ? <div className="text-sm text-red-600 space-y-2"><p role="alert">{error}</p><button type="button" onClick={() => void load()} className="text-blue-600 hover:underline">Try again</button></div> : active.length === 0 ? <p className="text-sm text-gray-500">No active liabilities yet. Add your first liability above.</p> : <div className="space-y-3">{active.map((item) => <LiabilityCard key={item.id} item={item} historyOpen={historyTarget?.id === item.id} onEdit={openEdit} onBalance={openBalanceUpdate} onRecord={openRecord} onHistory={toggleHistory} onAsOf={openAsOf} onArchive={() => void setArchived(item, true)} />)}</div>}
      </section>

      {showArchived && !loading && !error && (
        <section className="space-y-3 pt-2 border-t">
          <h2 className="text-lg font-semibold text-gray-600">Archived liabilities</h2>
          {archived.length === 0 ? <p className="text-sm text-gray-500">No archived liabilities.</p> : archived.map((item) => <div key={item.id} className="bg-gray-50 border rounded-xl p-4 flex items-start justify-between gap-4 flex-wrap"><div><p className="font-medium text-gray-600">{item.name}</p><p className="text-sm text-gray-500">{typeLabel(item.liability_type)}{item.lender ? ` · ${item.lender}` : ""}</p><p className="text-sm text-gray-600">{item.balance === 0 ? "Paid off" : formatThb(item.balance)} · THB</p></div><div className="flex gap-3 text-sm flex-wrap items-center"><button type="button" aria-expanded={historyTarget?.id === item.id} onClick={() => toggleHistory(item)} className="text-blue-600 hover:underline">Balance history</button><button type="button" onClick={() => openAsOf(item)} className="text-blue-600 hover:underline">Balance on date</button><button type="button" onClick={() => void setArchived(item, false)} className="text-sm text-blue-600 hover:underline">Restore</button></div></div>)}
        </section>
      )}
    </div>
  );
}

function LiabilityCard({ item, historyOpen, onEdit, onBalance, onRecord, onHistory, onAsOf, onArchive }: { item: Liability; historyOpen: boolean; onEdit: (item: Liability) => void; onBalance: (item: Liability) => void; onRecord: (item: Liability) => void; onHistory: (item: Liability) => void; onAsOf: (item: Liability) => void; onArchive: () => void }) {
  return <div className="bg-white border rounded-xl p-4 shadow-sm space-y-3"><div className="flex items-start justify-between gap-4 flex-wrap"><div><p className="font-semibold">{item.name}</p><p className="text-sm text-gray-500">{typeLabel(item.liability_type)}{item.lender ? ` · ${item.lender}` : ""}</p><p className="text-lg font-medium mt-1">{item.balance === 0 ? "Paid off" : formatThb(item.balance)} <span className="text-xs text-gray-500">THB</span></p>{item.note && <p className="text-sm text-gray-500 mt-1">{item.note}</p>}<p className="text-xs text-gray-400 mt-1">{item.first_observation_on ? `History tracking started ${item.first_observation_on}` : "No balance history recorded yet"}</p></div><div className="flex gap-3 text-sm flex-wrap"><button type="button" onClick={() => onEdit(item)} className="text-blue-600 hover:underline">Edit</button><button type="button" onClick={() => onBalance(item)} className="text-blue-600 hover:underline">Update balance</button><button type="button" onClick={() => onRecord(item)} className="text-blue-600 hover:underline">Record balance</button><button type="button" aria-expanded={historyOpen} onClick={() => onHistory(item)} className="text-blue-600 hover:underline">Balance history</button><button type="button" onClick={() => onAsOf(item)} className="text-blue-600 hover:underline">Balance on date</button><button type="button" onClick={onArchive} className="text-red-600 hover:underline">Archive</button></div></div></div>;
}

function TypeSelect({ ariaLabel, value, onChange }: { ariaLabel: string; value: LiabilityType; onChange: (value: LiabilityType) => void }) {
  return <select aria-label={ariaLabel} value={value} onChange={(event) => onChange(event.target.value as LiabilityType)} className={inputClass}>{LIABILITY_TYPES.map((item) => <option key={item} value={item}>{typeLabel(item)}</option>)}</select>;
}

function Field({ label, children }: { label: string; children: React.ReactNode }) { return <label className="text-sm">{label}{children}</label>; }
function PrimaryButton({ children }: { children: React.ReactNode }) { return <button type="submit" className="bg-blue-600 text-white px-3 py-1.5 rounded text-sm hover:bg-blue-700">{children}</button>; }
function Cancel({ onClick }: { onClick: () => void }) { return <button type="button" onClick={onClick} className="text-sm text-gray-600">Cancel</button>; }
function Actions({ children }: { children: React.ReactNode }) { return <div className="flex gap-2 mt-3">{children}</div>; }
