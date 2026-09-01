import { afterEach, describe, expect, it, vi } from "vitest";

import { deletePortfolioInvestmentMandate } from "@/lib/api";

afterEach(() => {
  vi.unstubAllGlobals();
});

describe("portfolio investment mandate API", () => {
  it("accepts DELETE 204 without attempting JSON parsing", async () => {
    const json = vi.fn(() => { throw new SyntaxError("Unexpected end of JSON input"); });
    const fetchMock = vi.fn().mockResolvedValue({ status: 204, ok: true, json });
    vi.stubGlobal("fetch", fetchMock);

    await expect(deletePortfolioInvestmentMandate(9, 2)).resolves.toBeUndefined();

    expect(fetchMock).toHaveBeenCalledWith(
      "http://localhost:8000/portfolios/9/investment-mandates/2",
      expect.objectContaining({ method: "DELETE" }),
    );
    expect(json).not.toHaveBeenCalled();
  });
});
