import { describe, test, expect, vi, beforeEach } from "vitest";
import { lookupSnapshotDecision } from "@/lib/decisionLookup";

const { listExecutionDecisions } = vi.hoisted(() => ({ listExecutionDecisions: vi.fn() }));
vi.mock("@/lib/api", () => ({ listExecutionDecisions }));

const row = (over: Record<string, unknown> = {}) => ({ id: 1, portfolio_id: 4, recommendation_snapshot_id: 175, ...over });

beforeEach(() => { listExecutionDecisions.mockReset(); });

describe("lookupSnapshotDecision", () => {
  test("found: exactly this portfolio and snapshot", async () => {
    listExecutionDecisions.mockResolvedValue([row()]);
    expect(await lookupSnapshotDecision(4, 175)).toMatchObject({ status: "found", decision: { id: 1 } });
    expect(listExecutionDecisions).toHaveBeenCalledWith(4, undefined, 1, 175);
  });
  test("none: a verified empty filtered result", async () => {
    listExecutionDecisions.mockResolvedValue([]);
    expect(await lookupSnapshotDecision(4, 175)).toEqual({ status: "none" });
  });
  test("unavailable: request failure", async () => {
    listExecutionDecisions.mockRejectedValue(new Error("offline"));
    expect(await lookupSnapshotDecision(4, 175)).toEqual({ status: "unavailable", reason: "REQUEST_FAILED" });
  });
  test.each([[null], [undefined], [{}], ["x"], [42]])("unavailable: malformed response %j", async (payload) => {
    listExecutionDecisions.mockResolvedValue(payload);
    expect(await lookupSnapshotDecision(4, 175)).toEqual({ status: "unavailable", reason: "MALFORMED_RESPONSE" });
  });
  test.each([
    [{ recommendation_snapshot_id: 174 }],
    [{ portfolio_id: 5 }],
    [{ recommendation_snapshot_id: undefined }],
    [{ portfolio_id: undefined }],
  ])("unavailable: wrong identity %j", async (over) => {
    listExecutionDecisions.mockResolvedValue([row(over)]);
    expect(await lookupSnapshotDecision(4, 175)).toEqual({ status: "unavailable", reason: "IDENTITY_MISMATCH" });
  });
  test("unavailable: non-object rows", async () => {
    listExecutionDecisions.mockResolvedValue([null]);
    expect((await lookupSnapshotDecision(4, 175)).status).toBe("unavailable");
  });
  test("unavailable: an older backend ignoring the filter returns the newest unrelated page", async () => {
    listExecutionDecisions.mockResolvedValue(Array.from({ length: 50 }, (_, i) => row({ id: i, recommendation_snapshot_id: 100 + i })));
    expect(await lookupSnapshotDecision(4, 175)).toEqual({ status: "unavailable", reason: "IDENTITY_MISMATCH" });
  });
  test("unavailable: a page that mixes the target row with unrelated rows is not trusted", async () => {
    listExecutionDecisions.mockResolvedValue([row(), row({ id: 2, recommendation_snapshot_id: 3 })]);
    expect((await lookupSnapshotDecision(4, 175)).status).toBe("unavailable");
  });
});
