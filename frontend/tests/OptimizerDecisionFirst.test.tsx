import { act, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";
import { resolve } from "node:path";
import OptimizerPage from "@/app/optimizer/page";
import OptimizerDecisionSummary from "@/components/optimizer/OptimizerDecisionSummary";
import ExecutionPlanCard from "@/components/optimizer/ExecutionPlanCard";
import AuditorClaimFlag from "@/components/optimizer/AuditorClaimFlag";
import { DecisionActionPanel } from "@/components/optimizer/DecisionActionPanel";
import { assessment, economicRecommendation, scheduledTradeCount } from "@/lib/optimizerPresentation";
import type { OptimizerResult } from "@/lib/api";
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
