import { afterEach, describe, expect, it, vi } from "vitest";

import { runOptimizer } from "@/lib/api";

afterEach(() => {
  vi.unstubAllGlobals();
});

function mockFetch() {
  const fetchMock = vi.fn().mockResolvedValue({
    ok: true,
    status: 200,
    json: async () => ({}),
  });
  vi.stubGlobal("fetch", fetchMock);
  return fetchMock;
}

function requestBody(fetchMock: ReturnType<typeof mockFetch>): unknown {
  return JSON.parse(fetchMock.mock.calls[0][1].body as string);
}

describe("optimizer Goal constraint request wiring", () => {
  it("preserves the legacy body when no Goal argument is supplied", async () => {
    const fetchMock = mockFetch();

    await runOptimizer(7, "openai", "gpt-5", true);

    expect(requestBody(fetchMock)).toEqual({
      portfolio_id: 7,
      provider: "openai",
      model: "gpt-5",
      force_rebalance: true,
    });
  });

  it.each([undefined, null])("omits goal_constraint_goal_id for %s", async (goalId) => {
    const fetchMock = mockFetch();

    await runOptimizer(7, undefined, undefined, undefined, goalId);

    expect(requestBody(fetchMock)).toEqual({ portfolio_id: 7 });
  });

  it("sends the selected numeric Goal ID while preserving other fields", async () => {
    const fetchMock = mockFetch();

    await runOptimizer(7, "anthropic", "claude", true, 42);

    expect(requestBody(fetchMock)).toEqual({
      portfolio_id: 7,
      provider: "anthropic",
      model: "claude",
      force_rebalance: true,
      goal_constraint_goal_id: 42,
    });
  });

  it("uses the new selection and removes the field after deselection", async () => {
    const fetchMock = mockFetch();

    await runOptimizer(7, undefined, undefined, undefined, 42);
    await runOptimizer(7, undefined, undefined, undefined, 99);
    await runOptimizer(7, undefined, undefined, undefined, null);

    expect(JSON.parse(fetchMock.mock.calls[0][1].body as string)).toMatchObject({ goal_constraint_goal_id: 42 });
    expect(JSON.parse(fetchMock.mock.calls[1][1].body as string)).toMatchObject({ goal_constraint_goal_id: 99 });
    expect(JSON.parse(fetchMock.mock.calls[2][1].body as string)).toEqual({ portfolio_id: 7 });
  });
});
