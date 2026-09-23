import { render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import MujiDashboard from "@/components/operations-center/muji/MujiDashboard";
import type { OperationsCenterStatus } from "@/lib/api";

vi.mock("@/lib/api", () => ({
  listOptimizerHistory: vi.fn().mockResolvedValue([]),
  getTrustReport: vi.fn().mockResolvedValue(null),
}));

import { listOptimizerHistory, getTrustReport } from "@/lib/api";

const status: OperationsCenterStatus = {
  generated_at: "2026-09-23T00:00:00",
  portfolio_id: 1,
  portfolio_name: "My Portfolio",
  mode_capabilities: { modes: ["MUJI", "QUANT"], default_mode: "MUJI" },
  portfolio_summary: {
    portfolio_value: 1_250_000,
    daily_return_pct: 1.25,
    goal_target_value: 2_000_000,
    goal_progress_pct: 62.5,
    days_since_last_rebalance: 10,
    snapshot_date: "2026-09-22",
  },
  goal_profile: {
    portfolio_id: 1,
    configured: true,
    goal_type: "FINANCIAL_FREEDOM",
    goal_emoji: "🎯",
    goal_label_th: "อิสรภาพทางการเงิน",
    goal_target_value: 2_000_000,
    goal_target_date: "2035-01-01",
    goal_priority: "ESSENTIAL",
    goal_priority_label_th: "สำคัญมาก",
    risk_personality: "MODERATE",
    risk_personality_label_th: "ปานกลาง",
  },
  market: {
    regime: "BULL",
    confidence_pct: 80,
    transition_stability: "STABLE",
    vix_level: 14,
    regime_duration_days: 30,
    risk_level: "low",
    label_th: "ตลาดขาขึ้น",
    description_th: "ตลาดอยู่ในภาวะขาขึ้น",
    narrative: null,
  },
  optimizer: {
    last_run_at: "2026-09-20T00:00:00",
    optimizer_status: "NO_ACTION",
    consensus_status: "AGREE",
    consensus_decision: "NO_ACTION",
    consensus_score: 0.9,
    final_risk_level: "low",
    recommendation_summary_th: "ไม่ต้องดำเนินการ",
    recommended_action: null,
  },
  policy: null,
  agent_health: {
    market_data_station: { status: "GREEN", label_th: "", detail: "", detail_th: "" },
    macro_station: { status: "GREEN", label_th: "", detail: "", detail_th: "" },
    risk_desk: { status: "GREEN", label_th: "", detail: "", detail_th: "" },
    quant_corner: { status: "GREEN", label_th: "", detail: "", detail_th: "" },
    portfolio_lab: { status: "GREEN", label_th: "", detail: "", detail_th: "" },
    consensus_room: { status: "GREEN", label_th: "", detail: "", detail_th: "" },
  },
  muji_translation: {
    headline: "พอร์ตของคุณอยู่ในเกณฑ์ดี",
    summary: ["ทุกอย่างเรียบร้อยดี"],
    action_required: { required: false, action_th: "ไม่ต้องทำอะไรตอนนี้", severity: "INFO", link: null },
  },
};

afterEach(() => {
  vi.clearAllMocks();
});

function renderDashboard() {
  return render(
    <MujiDashboard
      status={status}
      portfolioId={1}
      optimizing={false}
      onRunOptimizer={vi.fn()}
    />
  );
}

describe("MujiDashboard — Portfolio Goal Duplication Cleanup", () => {
  it("no longer renders the Investment Goal section", () => {
    renderDashboard();
    expect(screen.queryByText("เป้าหมายการลงทุน")).not.toBeInTheDocument();
    expect(screen.queryByText("อิสรภาพทางการเงิน")).not.toBeInTheDocument();
  });

  it("no longer renders the Goal Progress section", () => {
    renderDashboard();
    expect(screen.queryByText("ความคืบหน้าสู่เป้าหมาย")).not.toBeInTheDocument();
    expect(screen.queryByText(/62\.5%/)).not.toBeInTheDocument();
  });

  it("no goal-only Edit action is present in this context", () => {
    renderDashboard();
    // "แก้ไข" (Edit) was the goal-card-only action; nothing else in this
    // dashboard uses that label.
    expect(screen.queryByText("แก้ไข")).not.toBeInTheDocument();
  });

  it("still renders portfolio value / today's change headline content", () => {
    renderDashboard();
    expect(screen.getByText("มูลค่าพอร์ตวันนี้")).toBeInTheDocument();
    expect(screen.getByText("การเปลี่ยนแปลงวันนี้")).toBeInTheDocument();
    expect(screen.getByText("฿1,250,000.00")).toBeInTheDocument();
  });

  it("still renders remaining portfolio insight content (today's overview + action)", async () => {
    renderDashboard();
    expect(screen.getByText("พอร์ตของคุณอยู่ในเกณฑ์ดี")).toBeInTheDocument();
    expect(screen.getByText("ทุกอย่างเรียบร้อยดี")).toBeInTheDocument();
    await waitFor(() => expect(getTrustReport).toHaveBeenCalledWith(1, 90));
    expect(listOptimizerHistory).toHaveBeenCalledWith(1);
  });
});
