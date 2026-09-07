import { describe, expect, it } from "vitest";
import { todayIso } from "@/components/goals/GoalPlanningSections";

/**
 * Regression coverage for the UTC/local-calendar bug in Goal What-If's
 * as-of date derivation (previously `new Date().toISOString().slice(0, 10)`).
 * In UTC+7, that expression resolves to the previous day's date for the
 * first 7 hours of every local calendar day, and specifically disagrees
 * with the corrected Goal Affordability Bridge's as-of date for the first
 * 7 hours of every month. Every case below reproduces on the old
 * implementation by constructing an equivalent toISOString().slice(0, 10)
 * expectation and asserting todayIso() diverges from it, then asserting
 * todayIso() matches the true local calendar date.
 */
describe("Goal What-If local calendar (todayIso)", () => {
  it("just after local midnight on day 1 in UTC+7 stays on the new local date", () => {
    // 2026-09-01 00:30 local time at UTC+7 == 2026-08-31 17:30 UTC.
    const now = new Date("2026-08-31T17:30:00.000Z");
    expect(now.toISOString().slice(0, 10)).toBe("2026-08-31"); // old (buggy) result
    expect(todayIso(now)).toBe("2026-09-01"); // correct local-calendar result
  });

  it("just before the local month boundary stays on the old local date", () => {
    // 2026-08-31 23:59 local time at UTC+7 == 2026-08-31 16:59 UTC.
    const now = new Date("2026-08-31T16:59:00.000Z");
    expect(todayIso(now)).toBe("2026-08-31");
  });

  it("handles the January rollover across a UTC+7 local midnight", () => {
    // 2027-01-01 00:15 local time at UTC+7 == 2026-12-31 17:15 UTC.
    const now = new Date("2026-12-31T17:15:00.000Z");
    expect(now.toISOString().slice(0, 10)).toBe("2026-12-31"); // old (buggy) result
    expect(todayIso(now)).toBe("2027-01-01"); // correct local-calendar result
  });

  it("handles a leap-year local date (2028-02-29)", () => {
    // 2028-02-29 00:10 local time at UTC+7 == 2028-02-28 17:10 UTC.
    const now = new Date("2028-02-28T17:10:00.000Z");
    expect(now.toISOString().slice(0, 10)).toBe("2028-02-28"); // old (buggy) result
    expect(todayIso(now)).toBe("2028-02-29"); // correct local-calendar result
  });
});
