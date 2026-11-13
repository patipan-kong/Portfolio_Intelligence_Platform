import { render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import ConsensusRoomCard from "@/components/operations-center/quant/ConsensusRoomCard";
import type { OperationsOptimizer } from "@/lib/api";

vi.mock("@/lib/api", () => ({
  listOptimizerHistory: vi.fn().mockResolvedValue([]),
}));

const NO_ACTION_TH = "ไม่ต้องดำเนินการ";
const COOLDOWN_TH = "พักคำแนะนำชั่วคราว";
const NOT_TRADED_TH = /ไม่ได้หมายความว่ามีการซื้อขายแล้ว/;

const base: OperationsOptimizer = {
  last_run_at: "2026-11-12T00:00:00",
  optimizer_status: "REBALANCE",
  consensus_status: "STRONG_CONSENSUS",
  consensus_decision: "REBALANCE",
  consensus_score: 83,
  final_risk_level: "low",
  recommendation_summary_th: "",
  recommended_action: null,
};

function renderCard(optimizer: Partial<OperationsOptimizer>) {
  return render(
    <ConsensusRoomCard
      portfolioId={1}
      optimizer={{ ...base, ...optimizer }}
      optimizing={false}
      onRunOptimizer={() => {}}
      daysSinceRebalance={null}
    />,
  );
}

afterEach(() => {
  vi.clearAllMocks();
});

describe("ConsensusRoomCard decision badge", () => {
  it("labels an ordinary cooldown as a paused recommendation, not 'no action needed'", () => {
    renderCard({ optimizer_status: "COOLDOWN_ACTIVE", consensus_decision: "COOLDOWN_ACTIVE" });
    expect(screen.queryByText(NO_ACTION_TH)).not.toBeInTheDocument();
    // Badge and status line both read as a cooldown.
    expect(screen.getAllByText(COOLDOWN_TH)).toHaveLength(2);
    expect(screen.queryByText("COOLDOWN_ACTIVE")).not.toBeInTheDocument();
    const badge = screen.getAllByText(COOLDOWN_TH)[0];
    expect(badge.className).not.toMatch(/emerald/);
    // The note says the pause does not mean a trade happened.
    expect(screen.getByText(NOT_TRADED_TH)).toBeInTheDocument();
  });

  it("keeps a verified risk conflict visible during a cooldown", () => {
    renderCard({
      optimizer_status: "COOLDOWN_ACTIVE",
      consensus_decision: "COOLDOWN_ACTIVE",
      consensus_status: "RISK_CONFLICT",
      final_risk_level: "high",
      recommended_action: "Address Risk Auditor's flags before executing any rebalancing.",
    });
    expect(screen.getByText("RISK_CONFLICT")).toBeInTheDocument();
    expect(screen.getByText("สูง")).toBeInTheDocument();
    expect(screen.getByText(/Address Risk Auditor's flags/)).toBeInTheDocument();
    expect(screen.queryByText(NO_ACTION_TH)).not.toBeInTheDocument();
    expect(screen.getByText(NOT_TRADED_TH)).toBeInTheDocument();
  });

  it.each([
    ["REBALANCE", "REBALANCE", "ควรปรับสัดส่วน", /blue/],
    ["NO_ACTION", "NO_ACTION", NO_ACTION_TH, /emerald/],
    ["REVIEW", "REBALANCE", "รอตรวจสอบ", /amber/],
  ] as const)("leaves the %s badge unchanged", (decision, status, label, colour) => {
    renderCard({ consensus_decision: decision, optimizer_status: status });
    const [badge] = screen.getAllByText(label);
    expect(badge.className).toMatch(colour);
    expect(screen.queryByText(NOT_TRADED_TH)).not.toBeInTheDocument();
  });

  it("keeps NO_REBALANCE_REQUIRED on its previous no-action badge", () => {
    renderCard({ consensus_decision: "NO_REBALANCE_REQUIRED", optimizer_status: "NO_REBALANCE_REQUIRED" });
    expect(screen.getByText(NO_ACTION_TH)).toBeInTheDocument();
  });

  it("degrades safely for missing or unrecognised decisions", () => {
    const { unmount } = renderCard({ consensus_decision: null, optimizer_status: null, consensus_status: null });
    expect(screen.queryByText(NO_ACTION_TH)).not.toBeInTheDocument();
    expect(screen.getByText("—")).toBeInTheDocument();
    unmount();
    renderCard({
      consensus_decision: "SOMETHING_NEW" as unknown as OperationsOptimizer["consensus_decision"],
      optimizer_status: null,
    });
    // An unknown decision no longer claims "no action needed".
    expect(screen.queryByText(NO_ACTION_TH)).not.toBeInTheDocument();
    expect(screen.queryByText(NOT_TRADED_TH)).not.toBeInTheDocument();
  });
});
