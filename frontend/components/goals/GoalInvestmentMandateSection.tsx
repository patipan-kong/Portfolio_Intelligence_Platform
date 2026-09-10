import Link from "next/link";
import type { GoalInvestmentMandate } from "@/lib/api";

export type GoalInvestmentMandateState = GoalInvestmentMandate[] | { error: string } | undefined;

export function GoalInvestmentMandateSection({ state }: { state: GoalInvestmentMandateState }) {
  return (
    <section className="bg-white border rounded-xl p-4 shadow-sm space-y-3" aria-labelledby="investment-mandate-heading">
      <h2 id="investment-mandate-heading" className="text-lg font-semibold">Investment mandate</h2>
      <p className="text-xs text-gray-500">Investment portfolios intentionally managed to serve this goal.</p>
      {state === undefined ? (
        <p className="text-sm text-gray-400">Loading investment mandate…</p>
      ) : "error" in state ? (
        <p role="alert" className="text-sm text-red-600">{state.error || "Unable to load investment mandate."}</p>
      ) : state.length === 0 ? (
        <p className="text-sm text-gray-500">No portfolio is currently mandated to this goal.</p>
      ) : (
        <ul className="space-y-2">
          {state.map((mandate) => (
            <li key={mandate.id} className="border rounded-lg px-3 py-2 text-sm text-gray-700">
              <Link href={`/portfolio?portfolio=${mandate.portfolio_id}`} className="text-blue-700 hover:underline">
                {mandate.portfolio_name ?? `Portfolio #${mandate.portfolio_id}`}
              </Link>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
