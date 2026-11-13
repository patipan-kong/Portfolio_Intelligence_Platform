import { act, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { resolve } from "node:path";
import OptimizerPage from "@/app/optimizer/page";
import OptimizerDecisionSummary from "@/components/optimizer/OptimizerDecisionSummary";
import ExecutionPlanCard from "@/components/optimizer/ExecutionPlanCard";
import AuditorClaimFlag from "@/components/optimizer/AuditorClaimFlag";
import { DecisionActionPanel } from "@/components/optimizer/DecisionActionPanel";
import { assessment, committeeDecisionPresentation, economicRecommendation, safeguardsRemovedAllTrades, scheduledTradeCount } from "@/lib/optimizerPresentation";
import type { OptimizerResult, TargetAllocation } from "@/lib/api";
import raw217 from "./fixtures/optimizer-217.json";
import raw218 from "./fixtures/optimizer-218.json";

const { api, router, report } = vi.hoisted(() => ({
  api: {
    runOptimizer: vi.fn(), listOptimizerHistory: vi.fn(), getOptimizerHistory: vi.fn(),
    listStrategyProfiles: vi.fn(), getPortfolioPersona: vi.fn(), updatePortfolioPersona: vi.fn(),
    listWealthGoals: vi.fn(), getDecisionMemoryTimeline: vi.fn(), getOperationsStatus: vi.fn(),
    listExecutionDecisions: vi.fn(), getExecutionDecision: vi.fn(), getExecutionDetail: vi.fn(),
    getShadowPerformanceSummary: vi.fn(), recordDecisionBySnapshot: vi.fn(),
    isUnresolvedPortfolioError: vi.fn(() => false),
  }, router: { replace: vi.fn(), push: vi.fn() }, report: vi.fn(),
}));
vi.mock("@/lib/api", () => api);
vi.mock("next/navigation", async () => {
  const { useSyncExternalStore } = await import("react");
  return {
    useSearchParams: () => new URLSearchParams(useSyncExternalStore(
      (notify) => { window.addEventListener("mock-navigation", notify); return () => window.removeEventListener("mock-navigation", notify); },
      () => window.location.search)),
    useRouter: () => router,
  };
});
let selectedPortfolio: number | null = 4;
const portfolios = [4, 5].map((id) => ({ id, name: id === 4 ? "TA" : "Other", cash_balance: 0, created_at: "2026-01-01" }));
const selectPortfolio = (id: number) => { selectedPortfolio = id; window.dispatchEvent(new Event("mock-selection")); };
vi.mock("@/lib/PortfolioContext", async () => {
  const { useSyncExternalStore } = await import("react");
  return { usePortfolio: () => ({ portfolios, selectPortfolio, reportUnresolvedPortfolio: report,
    currentSelection: useSyncExternalStore(
      (notify) => { window.addEventListener("mock-selection", notify); return () => window.removeEventListener("mock-selection", notify); },
      () => selectedPortfolio),
  }) };
});
vi.mock("@/components/WorkspaceScopeSwitcher", () => ({ default: () => <span>TA portfolio</span> }));
vi.mock("@/components/operations-center/quant/OperationsTimeline", () => ({ default: () => null }));

const fixture = (id: number) => structuredClone(id === 217 ? raw217 : raw218) as unknown as OptimizerResult;
function optedInHold(): OptimizerResult {
  const result = fixture(218);
  result.active_policy = { ...result.active_policy!, optimizer_policy_mode: "wealth.optimizer-muji.v2",
    strategy_selection_mode: "wealth.strategy-selection.v1" };
  result.consensus = { ...result.consensus!, consensus_type: "STRATEGIC_CONFLICT",
    consensus_decision: "REBALANCE" };
  result.strategy_selection = { version: "wealth.strategy-selection.v1", state: "SELECTED",
    selected_candidate_id: "hold-current", reason_codes: ["CAUTIONED_HOLD"],
    material_uncertainty: ["NO_ELIGIBLE_ACTION"], comparison_against_hold: "No defensible action established." };
  result.strategic_candidates = { version: "wealth.strategic-candidates.v1", status: "PREPARED_NOT_SELECTED",
    candidates: [{ id: "hold-current", family: "HOLD", eligibility_status: "ELIGIBLE", proposed_allocations: [] }] };
  return result;
}
const history = [218, 217].map((id) => ({ id, portfolio_name: "TA", analyzed_at: fixture(id).analyzed_at,
  swap_count: 0, optimizer_status: fixture(id).status, final_consensus_score: id === 218 ? 64 : 26 }));
function navigate(url: string) {
  window.history.replaceState(null, "", url);
  window.dispatchEvent(new Event("mock-navigation"));
}
function preview(name: string, container: HTMLElement) {
  const dir = process.env.OPTIMIZER_UX_PREVIEW_DIR;
  if (!dir) return;
  mkdirSync(dir, { recursive: true });
  // Existing dev CSS only; no Tailwind/Next build or live application request.
  const css = readFileSync(resolve(".next/static/css/app/layout.css"), "utf8");
  writeFileSync(resolve(dir, `${name}.html`), `<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>${css}</style></head><body class="bg-gray-50"><main class="max-w-7xl mx-auto p-4">${container.innerHTML}</main></body></html>`);
}
beforeEach(() => {
  vi.clearAllMocks(); localStorage.clear(); selectedPortfolio = 4;
  navigate("/optimizer?portfolio=4&history=218");
  router.replace.mockImplementation((url: string) => navigate(url));
  api.listOptimizerHistory.mockResolvedValue(history);
  api.getOptimizerHistory.mockImplementation(async (id: number) => fixture(id));
  api.listStrategyProfiles.mockResolvedValue({ profiles: [] });
  api.getPortfolioPersona.mockResolvedValue({ persona: "GROWTH" });
  api.listWealthGoals.mockResolvedValue([]);
  api.listExecutionDecisions.mockResolvedValue([]);
  api.getDecisionMemoryTimeline.mockResolvedValue([]);
  api.getOperationsStatus.mockResolvedValue({ portfolio_summary: { snapshot_date: null, days_since_last_rebalance: null } });
});

describe("Selected historical journeys", () => {
  it("keeps frozen Committee HOLD authoritative when legacy consensus conflicts and says REBALANCE", async () => {
    api.getOptimizerHistory.mockResolvedValue(optedInHold());
    render(<OptimizerPage />);
    const decision = await screen.findByTestId("committee-decision");
    expect(decision).toHaveTextContent("Decision owner: Committee · SELECTED");
    expect(decision).toHaveTextContent("Selected strategy: HOLD · hold-current");
    expect(screen.getByText("Legacy Consensus Assessment")).toBeInTheDocument();
    expect(screen.getByText("Strategic conflict (legacy assessment)")).toBeInTheDocument();
    expect(screen.queryByText("Human Review Required")).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: /Full Consensus Detail/ }));
    expect(screen.getByText("Legacy assessment result").parentElement).toHaveTextContent("REBALANCE");
  });

  it("retains the legacy consensus display without exact opt-in markers", async () => {
    const result = optedInHold();
    result.active_policy = { ...result.active_policy!, strategy_selection_mode: undefined };
    api.getOptimizerHistory.mockResolvedValue(result);
    render(<OptimizerPage />);
    await screen.findByText("Decision owner: Challenger");
    expect(screen.getByText("Committee Decision")).toBeInTheDocument();
    expect(screen.getByText("Human Review Required")).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: /Full Consensus Detail/ }));
    expect(screen.getByText("REBALANCE")).toBeInTheDocument();
  });

  it("does not substitute legacy consensus for missing frozen selection evidence", async () => {
    const result = optedInHold();
    result.strategy_selection = null;
    api.getOptimizerHistory.mockResolvedValue(result);
    render(<OptimizerPage />);
    await screen.findByText(/Selection Evidence Unavailable/);
    expect(screen.getByText("Legacy Consensus Assessment")).toBeInTheDocument();
    expect(screen.getByText("Strategic conflict (legacy assessment)")).toBeInTheDocument();
    expect(screen.queryByText("Human Review Required")).not.toBeInTheDocument();
    expect(screen.queryByText("Decision owner: Challenger")).not.toBeInTheDocument();
  });

  it("keeps the per-run Committee opt-in off for history and sends it only when checked", async () => {
    api.runOptimizer.mockResolvedValue(fixture(218));
    render(<OptimizerPage />);
    await screen.findByText("Keep held positions unchanged");
    const toggle = screen.getByRole("checkbox", { name: /Use Committee strategy selection for this run/ });
    expect(toggle).not.toBeChecked();
    expect(api.runOptimizer).not.toHaveBeenCalled();
    fireEvent.click(screen.getByRole("button", { name: "Run Optimizer" }));
    await waitFor(() => expect(api.runOptimizer).toHaveBeenCalledWith(4, undefined, undefined, undefined, null, false));
    fireEvent.click(toggle);
    fireEvent.click(screen.getByRole("button", { name: "Run Optimizer" }));
    await waitFor(() => expect(api.runOptimizer).toHaveBeenLastCalledWith(4, undefined, undefined, undefined, null, true));
  });

  it("shows selected Committee evidence, HOLD comparison and safeguard changes", () => {
    const result = fixture(218);
    result.active_policy = { ...result.active_policy!, optimizer_policy_mode: "wealth.optimizer-muji.v2",
      strategy_selection_mode: "wealth.strategy-selection.v1" };
    result.strategy_selection = { version: "wealth.strategy-selection.v1", state: "SELECTED",
      selected_candidate_id: "proposal-a", supporting_evidence_refs: ["symbol:AAA:signal"],
      opposing_evidence_refs: ["regime:regime"], comparison_against_hold: "Lower thesis risk than HOLD.",
      decision_rationale: "Raise cash.", material_uncertainty: ["Timing uncertain"],
      reason_codes: ["COMMITTEE_SELECTED"], downstream_outcome: { status: "ALTERED_BY_SAFEGUARDS" } };
    result.strategic_candidates = { version: "wealth.strategic-candidates.v1", status: "PREPARED_NOT_SELECTED",
      observed_evidence_catalog: { "regime:regime": "DOWNTURN" }, candidates: [{
        id: "proposal-a", family: "RAISE_CASH", eligibility_status: "ELIGIBLE",
        observed_evidence_refs: { "symbol:AAA:signal": "SELL" }, proposed_allocations: [{
          symbol: "AAA", action: "SELL", current_weight: 50, target_weight: 0,
          allocation_change_percent: -50, estimated_amount: -5000, reason: "Frozen SELL signal",
        }],
      }] };
    result.candidate_audit = { status: "AVAILABLE", reviews: {
      "proposal-a": { supporting_refs: ["symbol:AAA:signal"], opposing_refs: ["regime:regime"] },
    } };
    result.target_allocations = [{ symbol: "AAA", action: "SELL", current_weight: 50,
      target_weight: 10, allocation_change_percent: -40, estimated_amount: -4000, reason: "Frozen SELL signal" }];
    const { rerender } = render(<OptimizerDecisionSummary result={result} historyId={8} historical loading={false} />);
    const decision = screen.getByTestId("committee-decision");
    expect(decision).toHaveTextContent("Decision owner: Committee");
    expect(decision).toHaveTextContent("RAISE CASH · proposal-a");
    expect(decision).toHaveTextContent("Lower thesis risk than HOLD");
    expect(decision).toHaveTextContent("symbol:AAA:signal = SELL");
    expect(decision).toHaveTextContent("regime:regime = DOWNTURN");
    expect(decision).toHaveTextContent("Proposed allocation: SELL AAA 0%");
    expect(decision).toHaveTextContent("Effective post-safeguard allocation: SELL AAA 10%");
    expect(screen.getByText(/Stored legacy consensus assessment/)).toBeInTheDocument();
    result.candidate_audit.reviews!["proposal-a"].supporting_refs = [];
    rerender(<OptimizerDecisionSummary result={{ ...result }} historyId={8} historical loading={false} />);
    expect(screen.getByText(/Selection Evidence Unavailable/)).toBeInTheDocument();
  });

  it.each(["ABSTAINED", "HUMAN_REVIEW_REQUIRED"] as const)("shows %s without selected action", (state) => {
    const result = fixture(218);
    result.active_policy = { ...result.active_policy!, optimizer_policy_mode: "wealth.optimizer-muji.v2",
      strategy_selection_mode: "wealth.strategy-selection.v1" };
    result.strategy_selection = { version: "wealth.strategy-selection.v1", state,
      selected_candidate_id: null, reason_codes: ["AUDITOR_UNAVAILABLE"], material_uncertainty: ["Missing NAV"] };
    result.strategic_candidates = { version: "wealth.strategic-candidates.v1", status: "PREPARED_NOT_SELECTED", candidates: [] };
    render(<OptimizerDecisionSummary result={result} historyId={8} historical loading={false} />);
    expect(screen.getByTestId("committee-decision")).toHaveTextContent(state.replace(/_/g, " "));
    expect(screen.getByTestId("committee-decision")).toHaveTextContent("AUDITOR_UNAVAILABLE");
    expect(screen.getByTestId("committee-decision")).not.toHaveTextContent("Selected strategy:");
  });

  it("distinguishes selected HOLD, unavailable evidence, and non-opt-in Challenger history", () => {
    const result = fixture(218);
    result.active_policy = { ...result.active_policy!, optimizer_policy_mode: "wealth.optimizer-muji.v2",
      strategy_selection_mode: "wealth.strategy-selection.v1" };
    result.strategy_selection = { version: "wealth.strategy-selection.v1", state: "SELECTED",
      selected_candidate_id: "hold-current", reason_codes: ["CAUTIONED_HOLD"],
      material_uncertainty: ["Auditor unavailable"], comparison_against_hold: "Wait for evidence." };
    result.strategic_candidates = { version: "wealth.strategic-candidates.v1", status: "PREPARED_NOT_SELECTED",
      candidates: [{ id: "hold-current", family: "HOLD", eligibility_status: "ELIGIBLE", proposed_allocations: [] }] };
    const { rerender } = render(<OptimizerDecisionSummary result={result} historyId={8} historical loading={false} />);
    expect(screen.getByTestId("committee-decision")).toHaveTextContent("no actionable alternative was preferred");
    result.strategy_selection = null;
    rerender(<OptimizerDecisionSummary result={{ ...result }} historyId={8} historical loading={false} />);
    expect(screen.getByText(/Selection Evidence Unavailable/)).toBeInTheDocument();
    result.active_policy = { ...result.active_policy!, strategy_selection_mode: undefined };
    rerender(<OptimizerDecisionSummary result={{ ...result }} historyId={8} historical loading={false} />);
    expect(screen.getByText("Decision owner: Challenger")).toBeInTheDocument();
  });

  it("renders malformed frozen references and candidate rows as unavailable", () => {
    const result = fixture(218);
    result.active_policy = { ...result.active_policy!, optimizer_policy_mode: "wealth.optimizer-muji.v2",
      strategy_selection_mode: "wealth.strategy-selection.v1" };
    result.strategy_selection = { version: "wealth.strategy-selection.v1", state: "SELECTED",
      selected_candidate_id: "hold-current", reason_codes: [], material_uncertainty: [],
      supporting_evidence_refs: "invalid" as unknown as string[] };
    result.strategic_candidates = { version: "wealth.strategic-candidates.v1",
      status: "PREPARED_NOT_SELECTED", candidates: [{ id: "hold-current", family: "HOLD",
        eligibility_status: "ELIGIBLE", proposed_allocations: [] }] };
    const { rerender } = render(<OptimizerDecisionSummary result={result} historyId={8} historical loading={false} />);
    expect(screen.getByText(/Selection Evidence Unavailable/)).toBeInTheDocument();
    result.strategy_selection.supporting_evidence_refs = [];
    result.strategic_candidates.candidates = [null] as unknown as typeof result.strategic_candidates.candidates;
    rerender(<OptimizerDecisionSummary result={{ ...result }} historyId={8} historical loading={false} />);
    expect(screen.getByText(/Selection Evidence Unavailable/)).toBeInTheDocument();
  });
  it("shows V2 recommendation separately from advisory schedule and unavailable estimates", () => {
    const result = fixture(218);
    result.active_policy = { ...result.active_policy!, optimizer_policy_mode: "wealth.optimizer-muji.v2" };
    result.target_allocations = [{ symbol: "AAA.BK", action: "SELL", reason: "Recorded thesis",
      current_weight: 10, target_weight: 0, allocation_change_percent: -10, estimated_amount: -10000 }];
    result.market_regime = null;
    result.goal_recommendation_constraints = undefined;
    result.no_action_summary = null;
    result.execution_optimization = null;
    render(<OptimizerDecisionSummary result={result} historyId={8} historical loading={false} />);
    const primary = screen.getByTestId("muji-primary-result");
    expect(within(primary).getByText(/SELL AAA.BK/).closest("li")).toHaveTextContent("Schedule unavailable");
    expect(within(primary).getByText(/Goal evidence unavailable/)).toBeInTheDocument();
    expect(within(primary).getByText(/Quantified HOLD comparison unavailable/)).toBeInTheDocument();
    expect(within(primary).getByText(/Estimated monetary impact unavailable/)).toBeInTheDocument();
  });

  it("labels a V2 monetary sale and per-side friction as estimates", () => {
    const result = fixture(218);
    result.active_policy = { ...result.active_policy!, optimizer_policy_mode: "wealth.optimizer-muji.v2" };
    result.target_allocations = [{ symbol: "AAA.BK", action: "SELL", reason: "Recorded thesis",
      current_weight: 10, target_weight: 0, allocation_change_percent: -10, estimated_amount: -10000 }];
    result.action_summary = { sell: [{ symbol: "AAA.BK", allocation_change_percent: -10 }],
      reduce: [], accumulate: [], new_position: [], hold: [] };
    result.execution_optimization = { cash_available: 1000, total_buy_deployment: 0,
      funding_gap: 0, idle_cash_after: 10985, scheduled_buys: {},
      scheduled_changes: { "AAA.BK": -10000 }, estimated_trade_costs: { "AAA.BK": 15 },
      trades: [{ symbol: "AAA.BK", action: "SELL", reason: "INVESTMENT_THESIS",
        necessity: "DISCRETIONARY", execution_role: "STANDALONE", execution_state: "FULL",
        full_recommended_amount: 10000, executed_amount: 10000, note: "Frozen signal" }] };
    render(<OptimizerDecisionSummary result={result} historyId={8} historical loading={false} />);
    const primary = screen.getByTestId("muji-primary-result");
    expect(within(primary).getByText(/SELL AAA.BK/).closest("li")).toHaveTextContent("Scheduled advisory THB 10,000");
    expect(within(primary).getByText(/Estimated trading friction/)).toHaveTextContent("0.15% per side");
    expect(within(primary).getByText(/Estimated trading friction/)).toHaveTextContent("THB 15");
    expect(within(primary).getByText(/CASH: estimated/)).toHaveTextContent("10,985");
  });

  it.each([
    [undefined, "Est. Turnover"],
    ["wealth.policy-evidence.v2", "Proposed Turnover"],
  ])("labels headline turnover for version %s", async (version, label) => {
    api.getOptimizerHistory.mockResolvedValue({
      ...fixture(218), execution_policy_version: version, portfolio_turnover_percent: 21.96,
    });
    render(<OptimizerPage />);
    const headline = await screen.findByText(label, { selector: "span" });
    expect(headline.parentElement).toHaveTextContent("22.0%");
  });

  it("puts the supported HOLD decision before controls, preserves 64, and synchronizes selection/reload", async () => {
    const { container, unmount } = render(<OptimizerPage />);
    await screen.findByText("Keep held positions unchanged");
    const summary = screen.getByRole("region", { name: "Selected analysis decision" });
    expect(within(summary).getByText("0")).toBeInTheDocument();
    expect(summary.compareDocumentPosition(screen.getByText("Control Panel")) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
    expect(within(summary).getByText(/64\/100/)).toBeInTheDocument();
    expect(screen.queryByText(/only reductions were suggested/)).not.toBeInTheDocument();
    await screen.findByRole("button", { name: /Approve Recommendation/ });
    preview("218", container);
    const earlier = screen.getAllByRole("button").find((b) => b.textContent?.includes("23:50"));
    expect(earlier).toBeDefined(); fireEvent.click(earlier!);
    await screen.findByText("REDUCE MICRON01.BK");
    expect(window.location.search).toBe("?portfolio=4&history=217");
    expect(within(summary).getByText("0")).toBeInTheDocument();
    expect(within(summary).getByText(/conflicts with your intent/)).toBeInTheDocument();
    expect(screen.getByText(/No reduction is scheduled today/)).toBeInTheDocument();
    expect(screen.queryByText("No trades recommended today")).not.toBeInTheDocument();
    expect(screen.getByText("Start new analysis with rebalance override")).toBeInTheDocument();
    await screen.findByRole("button", { name: /Approve Recommendation/ });
    preview("217", container);
    unmount(); render(<OptimizerPage />);
    await screen.findByText("REDUCE MICRON01.BK");
    expect(screen.getByRole("heading", { name: "Historical analysis #217" })).toBeInTheDocument();
    expect(api.runOptimizer).not.toHaveBeenCalled(); expect(api.recordDecisionBySnapshot).not.toHaveBeenCalled();
  });

  it("ignores late history responses during rapid switching", async () => {
    render(<OptimizerPage />); await screen.findByText("Keep held positions unchanged");
    let release: (r: OptimizerResult) => void = () => {};
    api.getOptimizerHistory.mockImplementation((id: number) => id === 217 ? new Promise((resolve) => { release = resolve; }) : Promise.resolve(fixture(id)));
    fireEvent.click(screen.getAllByRole("button").find((b) => b.textContent?.includes("23:50"))!);
    await waitFor(() => expect(window.location.search).toContain("217"));
    expect(screen.queryByText("Keep held positions unchanged")).not.toBeInTheDocument();
    fireEvent.click(screen.getAllByRole("button").find((b) => b.textContent?.includes("11:48"))!);
    await screen.findByText("Keep held positions unchanged");
    await act(async () => release(fixture(217)));
    expect(window.location.search).toContain("218");
    expect(screen.queryByText("REDUCE MICRON01.BK")).not.toBeInTheDocument();
  });

  it("responds to URL navigation and reloads after clearing portfolio selection", async () => {
    render(<OptimizerPage />); await screen.findByText("Keep held positions unchanged");
    act(() => navigate("/optimizer?portfolio=4&history=217"));
    expect(screen.queryByText("Keep held positions unchanged")).not.toBeInTheDocument();
    await screen.findByText("REDUCE MICRON01.BK");
    act(() => { selectedPortfolio = null; window.dispatchEvent(new Event("mock-selection")); });
    expect(screen.queryByText("REDUCE MICRON01.BK")).not.toBeInTheDocument();
    act(() => selectPortfolio(4));
    await screen.findByText("REDUCE MICRON01.BK");
    act(() => navigate("/optimizer?portfolio=4&history=invalid"));
    expect(screen.queryByText("REDUCE MICRON01.BK")).not.toBeInTheDocument();
    await screen.findByRole("alert");
    expect(api.runOptimizer).not.toHaveBeenCalled();
  });

  it("does not substitute latest history for a missing shared run", async () => {
    navigate("/optimizer?portfolio=4&history=999"); render(<OptimizerPage />);
    await screen.findByRole("alert");
    expect(screen.queryByText("Keep held positions unchanged")).not.toBeInTheDocument();
    expect(window.location.search).toContain("999");
  });

  it("resolves the shared portfolio and allows an explicit subsequent portfolio switch", async () => {
    selectedPortfolio = 5; render(<OptimizerPage />);
    await screen.findByText("Keep held positions unchanged"); expect(selectedPortfolio).toBe(4);
    api.listOptimizerHistory.mockImplementation(async (id: number) => id === 4 ? history : []);
    act(() => selectPortfolio(5));
    await waitFor(() => expect(window.location.search).toBe("?portfolio=5"));
    expect(screen.queryByText("Keep held positions unchanged")).not.toBeInTheDocument();
  });

  it("qualifies historical narratives and renders legacy warnings neutrally without rewriting scores", async () => {
    const original = JSON.stringify(raw218);
    const { container } = render(<OptimizerPage />); await screen.findByText("Keep held positions unchanged");
    fireEvent.click(screen.getByRole("button", { name: /AI reasoning and evidence/ }));
    expect(screen.getAllByText("Historical model reasoning — policy claims not independently verified")).toHaveLength(2);
    const labels = screen.getAllByText("[Historical model flag — not independently verified]");
    expect(labels).toHaveLength(2); labels.forEach((label) => expect(label.parentElement).not.toHaveClass("text-red-700"));
    fireEvent.click(screen.getByRole("button", { name: /Full Consensus Detail/ }));
    expect(screen.getByText(/Recorded historical recommendation — model claims not independently verified/)).toBeInTheDocument();
    expect(screen.getByText("39")).toBeInTheDocument();
    expect(JSON.stringify(raw218)).toBe(original);
    preview("218-evidence", container);
  });
});

describe("Unavailable evidence and action safety", () => {
  it("shows unscored sector commentary separately from Challenger agreement", async () => {
    const r = fixture(218);
    r.layer2_result = {
      ...r.layer2_result,
      agrees_with_layer1: true,
      disagreements: [],
      unscored_comments: ["Technology exceeds the sector threshold"],
    };
    api.getOptimizerHistory.mockResolvedValue(r);
    render(<OptimizerPage />);
    fireEvent.click(await screen.findByRole("button", { name: /AI reasoning and evidence/ }));
    const commentary = screen.getByText("Unscored Challenger commentary").parentElement!;
    expect(within(commentary).getByText("Technology exceeds the sector threshold")).toBeInTheDocument();
    expect(screen.getByText("✓ Agrees")).toBeInTheDocument();
    expect(screen.queryByText("Challenger disagrees with Strategist")).not.toBeInTheDocument();
  });

  it("does not imply reductions were suggested for a HOLD-only result at the position limit", async () => {
    const r = fixture(218); r.max_reached = true;
    api.getOptimizerHistory.mockResolvedValue(r); render(<OptimizerPage />);
    await screen.findByText("Keep held positions unchanged");
    expect(screen.getByText("Position limit reached")).toBeInTheDocument();
    expect(screen.queryByText(/only reductions\/swaps suggested/)).not.toBeInTheDocument();
  });
  it("distinguishes a just-completed response from a historical read", () => {
    render(<OptimizerDecisionSummary result={fixture(218)} historyId={219} historical={false} loading={false} />);
    expect(screen.getByRole("heading", { name: "Analysis just completed #219" })).toBeInTheDocument();
    expect(screen.getByText(/Bangkok time/)).toBeInTheDocument();
    expect(api.runOptimizer).not.toHaveBeenCalled();
  });
  it("never fabricates recommendation, zero trades or a score from NO_ACTION status", () => {
    const r = fixture(218); delete r.target_allocations; delete r.action_summary; delete r.consensus; delete r.final_consensus_score;
    render(<OptimizerDecisionSummary result={r} historyId={218} historical loading={false} />);
    expect(screen.getByText("Recommendation unavailable")).toBeInTheDocument();
    expect(screen.getByText(/execution evidence missing/)).toBeInTheDocument();
    expect(screen.getByText(/Consensus assessment unavailable/)).toBeInTheDocument();
    expect(screen.queryByText("0")).not.toBeInTheDocument();
    expect(assessment(NaN)).toBeNull();
  });
  it("preserves deferred economic reduction independently of scheduling status", () => {
    const r = fixture(217); r.status = "NO_ACTION";
    expect(economicRecommendation(r)).toBe("REDUCE MICRON01.BK"); expect(scheduledTradeCount(r)).toBe(0);
    delete r.execution_optimization; expect(scheduledTradeCount(r)).toBeNull();
  });
  it("does not accept partial execution summaries as zero-trade evidence", () => {
    const r = fixture(218); r.action_summary = { hold: [] } as never;
    render(<ExecutionPlanCard result={r} />);
    expect(screen.getByText(/Scheduled trades unavailable/)).toBeInTheDocument();
    expect(screen.queryByText("No trades scheduled in this plan")).not.toBeInTheDocument();
  });
  it("rejects duplicate scheduling identities and does not reconstruct suppressed recommendations", () => {
    const r = fixture(218);
    r.action_summary!.hold.push({ symbol: "BH.BK" } as never, { symbol: "BH.BK" } as never);
    expect(scheduledTradeCount(r)).toBeNull();
    r.target_allocations![0].noise_suppressed = true;
    expect(economicRecommendation(r)).toContain("Original economic recommendation unavailable");
  });
  it("missing risk level and score stay unavailable in detailed consensus", async () => {
    const r = fixture(218); delete r.consensus!.final_risk_level; delete r.consensus!.risk_alignment_score;
    delete r.consensus!.consensus_strength_score; delete r.layer3_result!.final_risk_level;
    api.getOptimizerHistory.mockResolvedValue(r); render(<OptimizerPage />);
    await screen.findByText("Keep held positions unchanged");
    fireEvent.click(screen.getByRole("button", { name: /Full Consensus Detail/ }));
    expect(screen.getAllByText("Unavailable").length).toBeGreaterThan(0);
    expect(screen.getByText("Historical model risk").parentElement).toHaveTextContent("UNAVAILABLE");
    expect(screen.getByText("Historical model risk level").parentElement).toHaveTextContent("UNAVAILABLE");
    expect(screen.queryByText(/Stored consensus assessment: 0/)).not.toBeInTheDocument();
  });
  it("failed decision loading disables recording until a successful retry", async () => {
    api.listExecutionDecisions.mockRejectedValueOnce(new Error("offline")).mockResolvedValue([]);
    render(<DecisionActionPanel snapshotId={174} portfolioId={4} />);
    await screen.findByText(/Owner decision status unavailable/);
    expect(screen.queryByRole("button", { name: /Approve/ })).not.toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: "Retry decision status" }));
    await screen.findByRole("button", { name: /Approve/ });
    expect(screen.getByText(/does not place trades or execute this plan/)).toBeInTheDocument();
    expect(api.recordDecisionBySnapshot).not.toHaveBeenCalled();
  });
  it("keeps truncated decision lookup unavailable instead of claiming no prior decision", async () => {
    api.listExecutionDecisions.mockResolvedValue(Array.from({ length: 50 }, (_, i) => ({ id: i, recommendation_snapshot_id: i })));
    render(<DecisionActionPanel snapshotId={174} portfolioId={4} />);
    await screen.findByText(/Owner decision status unavailable/);
    expect(screen.queryByRole("button", { name: /Approve/ })).not.toBeInTheDocument();
  });
  it("does not reopen recording after a successful mocked write with failed read-back", async () => {
    api.listExecutionDecisions.mockResolvedValueOnce([]).mockRejectedValueOnce(new Error("read-back offline"));
    api.recordDecisionBySnapshot.mockResolvedValue({});
    render(<DecisionActionPanel snapshotId={174} portfolioId={4} />);
    fireEvent.click(await screen.findByRole("button", { name: /Approve Recommendation/ }));
    fireEvent.click(screen.getByRole("button", { name: /Confirm/ }));
    await screen.findByText(/Owner decision status unavailable/);
    expect(screen.queryByRole("button", { name: /Approve/ })).not.toBeInTheDocument();
    expect(api.recordDecisionBySnapshot).toHaveBeenCalledTimes(1);
  });
  it("distinguishes verified, opinion and advisory evidence and keeps raw provenance expandable", () => {
    const flag = { symbol: "BH.BK", severity: "HIGH", issue: "Observation" } as const;
    render(<><AuditorClaimFlag flag={{ ...flag, validation_status: "VERIFIED", scoring_eligible: true, provenance: { source: "policy" } }} />
      <AuditorClaimFlag flag={{ ...flag, validation_status: "MODEL_OPINION", scoring_eligible: false }} />
      <AuditorClaimFlag flag={{ ...flag, validation_status: "ADVISORY", scoring_eligible: false }} /></>);
    expect(screen.getByText("[Verified restriction]")).toBeInTheDocument();
    expect(screen.getByText("[Model investment opinion — unscored]")).toBeInTheDocument();
    expect(screen.getByText("[Advisory — unscored]")).toBeInTheDocument();
    expect(screen.getByText("Evidence provenance").parentElement).not.toHaveAttribute("open");
  });
});

describe("Committee primary summary and technical details", () => {
  const withRegime = (result: OptimizerResult, regime: string) => {
    result.market_regime = { regime, confidence_pct: 80 } as OptimizerResult["market_regime"];
    return result;
  };
  const renderSummary = (result: OptimizerResult) =>
    render(<OptimizerDecisionSummary result={result} historyId={244} historical loading={false} />);

  it("leads with a plain-language HOLD recommendation derived from the run, with details collapsed", () => {
    renderSummary(withRegime(optedInHold(), "HIGH_VOLATILITY"));
    const primary = screen.getByTestId("committee-primary-summary");
    expect(primary).toHaveTextContent("Hold Current Portfolio");
    expect(primary).toHaveTextContent("Keep the current portfolio unchanged.");
    expect(primary).toHaveTextContent("Market volatility is high.");
    expect(primary).toHaveTextContent("does not establish that rebalancing would be better");
    expect(primary).toHaveTextContent("not a guarantee");
    expect(within(primary).getByText("Scheduled trades")).toBeInTheDocument();
    expect(within(primary).getByText("Estimated cash after plan")).toBeInTheDocument();
    for (const code of ["CAUTIONED_HOLD", "NO_ELIGIBLE_ACTION", "hold-current", "Committee · SELECTED"])
      expect(primary).not.toHaveTextContent(code);
    const details = screen.getByTestId("technical-details") as HTMLDetailsElement;
    expect(details.open).toBe(false);
    expect(details).toHaveTextContent("Decision owner: Committee · SELECTED");
    expect(details).toHaveTextContent("CAUTIONED_HOLD");
    expect(details).toHaveTextContent("Stored legacy consensus assessment");
  });

  it("does not hardcode the HOLD wording or regime sentence", () => {
    const result = withRegime(optedInHold(), "RISK_ON");
    renderSummary(result);
    const primary = screen.getByTestId("committee-primary-summary");
    expect(primary).not.toHaveTextContent("Market volatility is high");
    expect(primary).toHaveTextContent("risk-on");
  });

  it("shows plain uncertainty text and caps visible cautions", () => {
    const result = optedInHold();
    result.strategy_selection!.material_uncertainty = ["AUDITOR_UNAVAILABLE", "SOMETHING_NEW_CODE", "Free text note", "MATERIAL_CONFLICT_UNRESOLVED"];
    renderSummary(result);
    const cautions = screen.getByTestId("committee-cautions");
    expect(cautions).toHaveTextContent("Auditor review was unavailable.");
    expect(cautions).toHaveTextContent("Something new code.");
    expect(cautions).not.toHaveTextContent("AUDITOR_UNAVAILABLE");
    expect(cautions).toHaveTextContent(/more caveats in technical details/);
  });

  it.each([["ABSTAINED", "No Recommendation"], ["HUMAN_REVIEW_REQUIRED", "Human Review Required"]] as const)(
    "presents %s without a selected action or holdings", (state, headline) => {
      const result = optedInHold();
      result.strategy_selection = { version: "wealth.strategy-selection.v1", state, selected_candidate_id: null,
        reason_codes: ["AUDITOR_UNAVAILABLE"], material_uncertainty: [] };
      result.strategic_candidates = { version: "wealth.strategic-candidates.v1", status: "PREPARED_NOT_SELECTED", candidates: [] };
      renderSummary(result);
      const primary = screen.getByTestId("committee-primary-summary");
      expect(primary).toHaveTextContent(headline);
      expect(primary).not.toHaveTextContent("Hold Current Portfolio");
      expect(within(primary).queryByText("Holdings")).not.toBeInTheDocument();
    });

  it("degrades gracefully for missing or malformed selection evidence without using legacy consensus", () => {
    const result = optedInHold();
    result.strategy_selection = null;
    const { rerender } = renderSummary(result);
    let primary = screen.getByTestId("committee-primary-summary");
    expect(primary).toHaveTextContent("Recommendation Unavailable");
    expect(primary).toHaveTextContent("Missing evidence does not mean low risk");
    expect(primary).not.toHaveTextContent("Hold Current Portfolio");
    expect(within(primary).queryByText("Holdings")).not.toBeInTheDocument();
    result.strategy_selection = { version: "wealth.strategy-selection.v1", state: "SELECTED",
      selected_candidate_id: "hold-current", reason_codes: "bad" as unknown as string[], material_uncertainty: [] };
    rerender(<OptimizerDecisionSummary result={{ ...result }} historyId={244} historical loading={false} />);
    primary = screen.getByTestId("committee-primary-summary");
    expect(primary).toHaveTextContent("Recommendation Unavailable");
  });

  it("lists each holding with its recommended action and scheduled amount", () => {
    const result = optedInHold();
    result.target_allocations = [{ symbol: "AAA.BK", action: "HOLD", current_weight: 10, target_weight: 10,
      allocation_change_percent: 0, estimated_amount: 0, reason: "r" }];
    renderSummary(result);
    const row = within(screen.getByTestId("committee-primary-summary")).getByText("AAA.BK").closest("li")!;
    expect(row).toHaveTextContent("Hold");
  });

  // Phase 4.7 D3 shape: Committee selects BUY BBB 20->30; the 15% execution cap
  // turns the effective row into HOLD, so no actionable trade remains.
  const row = (symbol: string, action: TargetAllocation["action"], current: number, target: number): TargetAllocation => ({
    symbol, action, current_weight: current, target_weight: target, allocation_change_percent: target - current,
    estimated_amount: (target - current) * 1000, reason: "Frozen observation", note: "" } as TargetAllocation);
  const committeeAltered = (effective: TargetAllocation[] | undefined, uncertainty: string[] = []) => {
    const result = optedInHold();
    result.strategy_selection = { version: "wealth.strategy-selection.v1", state: "SELECTED",
      selected_candidate_id: "proposal-b", supporting_evidence_refs: ["symbol:BBB:signal"], opposing_evidence_refs: [],
      comparison_against_hold: "Observed evidence favours this over waiting.", decision_rationale: "Act on the observed evidence.",
      material_uncertainty: uncertainty, reason_codes: ["COMMITTEE_SELECTED"],
      downstream_outcome: { status: "ALTERED_BY_SAFEGUARDS" } };
    result.strategic_candidates = { version: "wealth.strategic-candidates.v1", status: "PREPARED_NOT_SELECTED", candidates: [
      { id: "hold-current", family: "HOLD", eligibility_status: "ELIGIBLE", proposed_allocations: [] },
      { id: "proposal-b", family: "GROWTH_ROTATION", eligibility_status: "ELIGIBLE",
        observed_evidence_refs: { "symbol:BBB:signal": "ACCUMULATE" },
        proposed_allocations: [row("AAA", "HOLD", 60, 60), row("BBB", "BUY", 20, 30)] },
    ] };
    result.candidate_audit = { status: "AVAILABLE", reviews: {
      "proposal-b": { supporting_refs: ["symbol:BBB:signal"], opposing_refs: [] } } };
    result.target_allocations = effective;
    const actionable = (effective ?? []).filter((r) => r.action === "BUY");
    result.action_summary = { sell: [], reduce: [], new_position: [],
      accumulate: actionable.map((r) => ({ symbol: r.symbol, allocation_change_percent: r.allocation_change_percent })),
      hold: (effective ?? []).filter((r) => r.action === "HOLD").map((r) => ({ symbol: r.symbol, allocation_change_percent: 0 })) } as never;
    result.execution_optimization = { cash_available: 200000, total_buy_deployment: 0, funding_gap: 0, idle_cash_after: 200000,
      scheduled_buys: {}, scheduled_changes: {}, estimated_trade_costs: {}, trades: [] } as never;
    return result;
  };
  const neutralizedRows = () => [row("AAA", "HOLD", 60, 60), row("BBB", "HOLD", 20, 20)];

  it("presents a Committee selection fully neutralized by safeguards as HOLD and keeps provenance in details", () => {
    const result = committeeAltered(neutralizedRows(),
      ["AUDITOR_UNAVAILABLE", "MODEL_SCORE_ONLY_SUPPORT", "Timing uncertain", "MATERIAL_CONFLICT_UNRESOLVED"]);
    renderSummary(result);
    const primary = screen.getByTestId("committee-primary-summary");
    expect(primary).toHaveTextContent("Hold Current Portfolio");
    expect(primary).toHaveTextContent("The Committee selected a strategy, but downstream safeguards removed all proposed trades. No trades are scheduled.");
    expect(primary).not.toHaveTextContent("Growth rotation");
    expect(primary).not.toHaveTextContent("The Committee selected this plan over holding");
    expect(primary).not.toHaveTextContent("cautious default");
    expect(within(primary).getByText("Scheduled trades").nextElementSibling).toHaveTextContent(/^0$/);
    // Safeguard caution leads, so the three-caution cap cannot hide it.
    const cautions = screen.getByTestId("committee-cautions");
    expect(cautions.firstElementChild).toHaveTextContent("Safeguards changed the selected plan");
    expect(cautions).toHaveTextContent(/more caveats in technical details/);
    const details = screen.getByTestId("technical-details");
    const decision = within(details).getByTestId("committee-decision");
    expect(decision).toHaveTextContent("Decision owner: Committee · SELECTED");
    expect(decision).toHaveTextContent("Selected strategy: GROWTH ROTATION · proposal-b");
    expect(decision).toHaveTextContent("COMMITTEE_SELECTED");
    expect(decision).toHaveTextContent("Proposed allocation: HOLD AAA 60%; BUY BBB 30%");
    expect(decision).toHaveTextContent("Effective post-safeguard allocation: HOLD AAA 60%; HOLD BBB 20%");
    expect(decision).toHaveTextContent("Safeguards removed every proposed trade; no actionable trade remains");
    expect(decision).not.toHaveTextContent("Selection is a recommendation.");
    expect(economicRecommendation(result)).toBe("Keep held positions unchanged");
  });

  it("keeps the selected strategy for a partially altered plan where a trade survives", () => {
    const result = committeeAltered([row("AAA", "HOLD", 60, 60), row("BBB", "BUY", 20, 25)]);
    renderSummary(result);
    const primary = screen.getByTestId("committee-primary-summary");
    expect(primary).toHaveTextContent("Growth rotation");
    expect(primary).toHaveTextContent("The Committee selected this plan over holding the current portfolio.");
    expect(primary).not.toHaveTextContent("Hold Current Portfolio");
    expect(primary).not.toHaveTextContent("removed all proposed trades");
    expect(screen.getByTestId("committee-cautions")).toHaveTextContent("Safeguards changed the selected plan");
    const decision = screen.getByTestId("committee-decision");
    expect(decision).toHaveTextContent("Effective post-safeguard allocation: HOLD AAA 60%; BUY BBB 25%");
    expect(decision).not.toHaveTextContent("Safeguards removed every proposed trade");
    expect(decision).toHaveTextContent("Selection is a recommendation.");
  });

  it("keeps ordinary Committee HOLD presentation and claims nothing without effective rows", () => {
    const hold = optedInHold();
    expect(safeguardsRemovedAllTrades(committeeDecisionPresentation(hold))).toBe(false);
    renderSummary(hold);
    const primary = screen.getByTestId("committee-primary-summary");
    expect(primary).toHaveTextContent("Keep the current portfolio unchanged.");
    expect(primary).toHaveTextContent("not a guarantee");
    expect(primary).not.toHaveTextContent("removed all proposed trades");
    // Old/partial snapshots: missing, empty or unknown effective rows never qualify.
    for (const effective of [undefined, [], [row("BBB", "PENDING" as TargetAllocation["action"], 20, 20)]]) {
      expect(safeguardsRemovedAllTrades(committeeDecisionPresentation(committeeAltered(effective)))).toBe(false);
    }
    const unaltered = committeeAltered(neutralizedRows());
    unaltered.strategy_selection!.downstream_outcome = { status: "UNCHANGED" };
    expect(safeguardsRemovedAllTrades(committeeDecisionPresentation(unaltered))).toBe(false);
    expect(safeguardsRemovedAllTrades(committeeDecisionPresentation(committeeAltered(neutralizedRows())))).toBe(true);
  });

  it("leaves non-Committee MUJI and Challenger layouts unchanged", () => {
    const result = optedInHold();
    result.active_policy = { ...result.active_policy!, strategy_selection_mode: undefined };
    renderSummary(result);
    expect(screen.queryByTestId("committee-primary-summary")).not.toBeInTheDocument();
    expect(screen.queryByTestId("technical-details")).not.toBeInTheDocument();
    expect(screen.getByText("Decision owner: Challenger")).toBeInTheDocument();
    expect(screen.getByTestId("muji-primary-result")).toBeInTheDocument();
  });
});
