import type { ReactNode } from "react";
import Link from "next/link";
import type { ExecutionSymbolLinkedTransaction } from "@/lib/api";

function shortDate(iso: string): string {
  return new Date(iso).toLocaleDateString("en-GB", { day: "2-digit", month: "short", year: "2-digit" });
}

// DEM-01: renders the transactions already explicitly linked to a decision
// (Transaction.execution_decision_id) as drill-through links into their
// history row. A link here means only that association — never success,
// settlement, fill quality, or recommendation correctness. Shared by
// Execution Detail and the Report Card so both surfaces present identical
// evidence identically.
export default function TransactionEvidenceLinks({
  transactions,
  emptyFallback = null,
}: {
  transactions: ExecutionSymbolLinkedTransaction[];
  emptyFallback?: ReactNode;
}) {
  if (transactions.length === 0) return <>{emptyFallback}</>;
  return (
    <>
      {transactions.map((t, i) => (
        <span key={t.id}>
          {i > 0 && ", "}
          <Link
            href={`/history?transactionId=${t.id}`}
            className="text-xs text-blue-600 hover:underline whitespace-nowrap"
          >
            #{t.id} ({shortDate(t.transaction_date)})
          </Link>
        </span>
      ))}
    </>
  );
}
