"use client";

import { FormEvent, useEffect, useState } from "react";
import {
  createCashAccount,
  listCashAccounts,
  updateCashAccount,
  type CashAccount,
} from "@/lib/api";

const formatThb = (value: number) =>
  value.toLocaleString("th-TH", { style: "currency", currency: "THB", minimumFractionDigits: 2 });

function messageFor(error: unknown, fallback: string) {
  return error instanceof Error ? error.message : fallback;
}

export default function CashAccountsPage() {
  const [accounts, setAccounts] = useState<CashAccount[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [mutationError, setMutationError] = useState("");
  const [showArchived, setShowArchived] = useState(false);
  const [name, setName] = useState("");
  const [institution, setInstitution] = useState("");
  const [balance, setBalance] = useState("0");
  const [editing, setEditing] = useState<CashAccount | null>(null);
  const [balanceTarget, setBalanceTarget] = useState<CashAccount | null>(null);
  const [editName, setEditName] = useState("");
  const [editInstitution, setEditInstitution] = useState("");
  const [replacementBalance, setReplacementBalance] = useState("");

  async function load(includeArchived = showArchived) {
    setLoading(true);
    setError("");
    try {
      setAccounts(await listCashAccounts(includeArchived));
    } catch (err) {
      setError(messageFor(err, "Unable to load cash accounts."));
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void load(false);
    // The initial request intentionally loads active accounts only.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function handleCreate(event: FormEvent) {
    event.preventDefault();
    setMutationError("");
    const parsedBalance = Number(balance);
    if (!name.trim() || !Number.isFinite(parsedBalance) || parsedBalance < 0) {
      setMutationError("Enter an account name and a non-negative current balance.");
      return;
    }
    try {
      await createCashAccount({ name: name.trim(), institution: institution.trim() || null, currency: "THB", balance: parsedBalance });
      setName("");
      setInstitution("");
      setBalance("0");
      await load();
    } catch (err) {
      setMutationError(messageFor(err, "Unable to create cash account."));
    }
  }

  function openEdit(account: CashAccount) {
    setMutationError("");
    setEditing(account);
    setEditName(account.name);
    setEditInstitution(account.institution ?? "");
    setBalanceTarget(null);
  }

  async function handleEdit(event: FormEvent) {
    event.preventDefault();
    if (!editing) return;
    setMutationError("");
    if (!editName.trim()) {
      setMutationError("Account name cannot be blank.");
      return;
    }
    try {
      await updateCashAccount(editing.id, { name: editName.trim(), institution: editInstitution.trim() || null });
      setEditing(null);
      await load();
    } catch (err) {
      setMutationError(messageFor(err, "Unable to update cash account."));
    }
  }

  function openBalanceUpdate(account: CashAccount) {
    setMutationError("");
    setBalanceTarget(account);
    setReplacementBalance(String(account.balance));
    setEditing(null);
  }

  async function handleBalanceUpdate(event: FormEvent) {
    event.preventDefault();
    if (!balanceTarget) return;
    setMutationError("");
    const parsedBalance = Number(replacementBalance);
    if (!Number.isFinite(parsedBalance) || parsedBalance < 0) {
      setMutationError("Enter a non-negative current balance.");
      return;
    }
    try {
      await updateCashAccount(balanceTarget.id, { balance: parsedBalance });
      setBalanceTarget(null);
      await load();
    } catch (err) {
      setMutationError(messageFor(err, "Unable to update balance."));
    }
  }

  async function setArchived(account: CashAccount, isArchived: boolean) {
    setMutationError("");
    try {
      await updateCashAccount(account.id, { is_archived: isArchived });
      await load();
    } catch (err) {
      setMutationError(messageFor(err, isArchived ? "Unable to archive cash account." : "Unable to restore cash account."));
    }
  }

  async function toggleArchived() {
    const next = !showArchived;
    setShowArchived(next);
    await load(next);
  }

  const active = accounts.filter((account) => !account.is_archived);
  const archived = accounts.filter((account) => account.is_archived);

  return (
    <div className="space-y-6 max-w-3xl">
      <div>
        <h1 className="text-2xl font-bold">Cash Accounts</h1>
        <p className="text-sm text-gray-500 mt-1">Track the current observed balance of external cash accounts.</p>
      </div>

      <form onSubmit={handleCreate} className="bg-white border rounded-xl p-4 space-y-3 shadow-sm">
        <h2 className="font-semibold">Add cash account</h2>
        <div className="grid gap-3 sm:grid-cols-3">
          <label className="text-sm">Account name
            <input aria-label="Account name" value={name} onChange={(event) => setName(event.target.value)} className="mt-1 block w-full border rounded px-3 py-2" />
          </label>
          <label className="text-sm">Institution (optional)
            <input aria-label="Institution" value={institution} onChange={(event) => setInstitution(event.target.value)} className="mt-1 block w-full border rounded px-3 py-2" />
          </label>
          <label className="text-sm">Current balance
            <input aria-label="Initial balance" type="number" step="0.01" value={balance} onChange={(event) => setBalance(event.target.value)} className="mt-1 block w-full border rounded px-3 py-2" />
          </label>
        </div>
        <p className="text-xs text-gray-500">Currency: <strong>THB</strong> (fixed for Cash Accounts v1)</p>
        <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded text-sm hover:bg-blue-700">Add cash account</button>
      </form>

      {mutationError && <p role="alert" className="text-sm text-red-600">{mutationError}</p>}

      {editing && (
        <form onSubmit={handleEdit} className="bg-blue-50 border border-blue-200 rounded-xl p-4 space-y-3">
          <h2 className="font-semibold">Edit {editing.name}</h2>
          <div className="grid gap-3 sm:grid-cols-2">
            <label className="text-sm">Account name
              <input aria-label="Edit account name" value={editName} onChange={(event) => setEditName(event.target.value)} className="mt-1 block w-full border rounded px-3 py-2" />
            </label>
            <label className="text-sm">Institution
              <input aria-label="Edit institution" value={editInstitution} onChange={(event) => setEditInstitution(event.target.value)} className="mt-1 block w-full border rounded px-3 py-2" />
            </label>
          </div>
          <div className="flex gap-2"><button type="submit" className="bg-blue-600 text-white px-3 py-1.5 rounded text-sm">Save changes</button><button type="button" onClick={() => setEditing(null)} className="text-sm text-gray-600">Cancel</button></div>
        </form>
      )}

      {balanceTarget && (
        <form onSubmit={handleBalanceUpdate} className="bg-blue-50 border border-blue-200 rounded-xl p-4 space-y-3">
          <h2 className="font-semibold">Update balance — {balanceTarget.name}</h2>
          <label className="text-sm">Current observed balance (THB)
            <input aria-label="Replacement balance" type="number" step="0.01" value={replacementBalance} onChange={(event) => setReplacementBalance(event.target.value)} className="mt-1 block w-full max-w-xs border rounded px-3 py-2" />
          </label>
          <div className="flex gap-2"><button type="submit" className="bg-blue-600 text-white px-3 py-1.5 rounded text-sm">Save balance</button><button type="button" onClick={() => setBalanceTarget(null)} className="text-sm text-gray-600">Cancel</button></div>
        </form>
      )}

      <div className="flex items-center justify-between gap-3">
        <h2 className="text-lg font-semibold">Active accounts</h2>
        <button type="button" onClick={toggleArchived} className="text-sm text-blue-600 hover:underline">{showArchived ? "Hide archived" : "Show archived"}</button>
      </div>

      {loading ? <p className="text-sm text-gray-400">Loading cash accounts…</p> : error ? (
        <div className="text-sm text-red-600 space-y-2"><p>{error}</p><button type="button" onClick={() => void load()} className="text-blue-600 hover:underline">Try again</button></div>
      ) : active.length === 0 ? <p className="text-sm text-gray-500">No active cash accounts yet. Add your first account above.</p> : (
        <div className="space-y-3">
          {active.map((account) => <AccountCard key={account.id} account={account} onEdit={openEdit} onBalance={openBalanceUpdate} onArchive={() => void setArchived(account, true)} />)}
        </div>
      )}

      {showArchived && !loading && !error && (
        <section className="space-y-3 pt-2 border-t">
          <h2 className="text-lg font-semibold text-gray-600">Archived accounts</h2>
          {archived.length === 0 ? <p className="text-sm text-gray-500">No archived cash accounts.</p> : archived.map((account) => (
            <div key={account.id} className="bg-gray-50 border rounded-xl p-4 flex items-center justify-between gap-4">
              <div><p className="font-medium text-gray-600">{account.name}</p><p className="text-sm text-gray-500">{formatThb(account.balance)} · THB</p></div>
              <button type="button" onClick={() => void setArchived(account, false)} className="text-sm text-blue-600 hover:underline">Restore</button>
            </div>
          ))}
        </section>
      )}
    </div>
  );
}

function AccountCard({ account, onEdit, onBalance, onArchive }: { account: CashAccount; onEdit: (account: CashAccount) => void; onBalance: (account: CashAccount) => void; onArchive: () => void }) {
  return <div className="bg-white border rounded-xl p-4 shadow-sm flex items-center justify-between gap-4 flex-wrap">
    <div><p className="font-semibold">{account.name}</p>{account.institution && <p className="text-sm text-gray-500">{account.institution}</p>}<p className="text-lg font-medium mt-1">{formatThb(account.balance)} <span className="text-xs text-gray-500">THB</span></p></div>
    <div className="flex gap-3 text-sm"><button type="button" onClick={() => onEdit(account)} className="text-blue-600 hover:underline">Edit</button><button type="button" onClick={() => onBalance(account)} className="text-blue-600 hover:underline">Update balance</button><button type="button" onClick={onArchive} className="text-red-600 hover:underline">Archive</button></div>
  </div>;
}
