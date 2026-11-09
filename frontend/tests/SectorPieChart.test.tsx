import { expect, test, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import SectorPieChart from "@/components/SectorPieChart";

vi.mock("recharts", async (importOriginal) => ({
  ...await importOriginal<typeof import("recharts")>(),
  ResponsiveContainer: () => null,
}));

test("discloses mixed-source sector groups without changing their percentages", () => {
  render(<SectorPieChart breakdown={{
    total_value: 1000,
    sectors: [
      {
        sector: "Technology", value: 517, weight_pct: 51.7,
        stocks: ["GOOGL01.BK", "NVDA01.BK"], limit_pct: 60, status: "WARNING",
        classification_sources: ["registry_fact", "static_taxonomy"], classification_status: "provisional",
      },
      {
        sector: "Healthcare", value: 483, weight_pct: 48.3,
        stocks: ["BH.BK"], limit_pct: 50, status: "OK",
        classification_sources: ["registry_fact"], classification_status: "authoritative",
      },
    ],
  }} />);

  const cue = screen.getByText("Includes provisional groupings");
  expect(cue.parentElement).toHaveTextContent("Technology");
  expect(screen.getByText("51.7%")).toBeInTheDocument();
  expect(screen.getByText("48.3%")).toBeInTheDocument();
  expect(screen.getByText("Healthcare").parentElement).not.toHaveTextContent("provisional");
});
