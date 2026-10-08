import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import AuditorClaimFlag from "@/components/optimizer/AuditorClaimFlag";
import type { RiskFlag } from "@/lib/api";

const base: RiskFlag = { symbol: "BH.BK", issue: "Model claim", severity: "HIGH" };
describe("Auditor evidence attribution", () => {
  it("shows unsupported claims as unscored with provenance", () => {
    const { container } = render(<AuditorClaimFlag flag={{ ...base, validation_status: "UNSUPPORTED",
      scoring_eligible: false, provenance: "No deterministic breach evidence" }} />);
    expect(screen.getByText("[Unsupported — unscored]")).toBeInTheDocument();
    expect(screen.getByText(/No deterministic breach evidence/)).toBeInTheDocument();
    expect(container.firstChild).not.toHaveClass("text-red-700");
  });
  it("distinguishes opinions from verified restrictions", () => {
    render(<><AuditorClaimFlag flag={{ ...base, validation_status: "MODEL_OPINION", scoring_eligible: false }} />
      <AuditorClaimFlag flag={{ ...base, validation_status: "VERIFIED", provenance: { allowed_pct: 25 } }} /></>);
    expect(screen.getByText("[Model investment opinion — unscored]")).toBeInTheDocument();
    expect(screen.getByText("[Verified restriction]")).toBeInTheDocument();
    expect(screen.getByText(/allowed_pct/)).toBeInTheDocument();
  });
  it("attributes independently evidenced investment risk", () => {
    render(<AuditorClaimFlag flag={{ ...base, validation_status: "VERIFIED", scoring_eligible: true,
      claim_kind: "INVESTMENT_OBSERVATION", provenance: { source: "optimizer_timing.enrich_scores_with_timing" } }} />);
    expect(screen.getByText("[Evidence-backed investment risk]")).toBeInTheDocument();
    expect(screen.getByText(/optimizer_timing/)).toBeInTheDocument();
  });
  it("does not reinterpret legacy evidence", () => {
    render(<AuditorClaimFlag flag={base} />);
    expect(screen.getByText("[Historical model flag — not independently verified]")).toBeInTheDocument();
  });
});
