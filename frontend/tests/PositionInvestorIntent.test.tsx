import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

import PositionInvestorIntent from "@/components/PositionInvestorIntent";
import {
  listPositionIntents,
  putPositionIntent,
  type PositionIntent,
  type PositionIntentView,
} from "@/lib/api";

vi.mock("@/lib/api", () => ({
  listPositionIntents: vi.fn(),
  putPositionIntent: vi.fn(),
}));

const DISCLOSURE = "Investor Intent V1 is saved for your records only. It is not yet read or enforced by the portfolio optimizer, and it does not change current recommendations.";

const confirmed: PositionIntent = {
  id: 3, portfolio_id: 9, position_symbol: "PTT.BK", increase_prohibited: false,
  decrease_prohibited: true, soft_preference: "PREFER_KEEP", revision: 2, author_kind: "OWNER",
  created_at: "2026-10-07T00:00:00", updated_at: "2026-10-07T00:00:00",
};

function viewWith(): PositionIntentView {
  return {
    contract_version: "investor-intent.v1", portfolio_id: 9, enforced_by_optimizer: false,
    disclosure: DISCLOSURE,
    positions: [
      { position_symbol: "PIS.BK", currently_held: true, holding_started_at: "2026-10-01T00:00:00", legacy_allow_swap: false,
        legacy_lock_status: "LEGACY_LOCKED_INTENT_UNCONFIRMED", intent_status: "NO_CONFIRMED_INTENT", intent: null },
      { position_symbol: "PTT.BK", currently_held: true, holding_started_at: "2026-10-01T00:00:00", legacy_allow_swap: true,
        legacy_lock_status: null, intent_status: "CONFIRMED", intent: confirmed },
    ],
  };
}

const listMock = vi.mocked(listPositionIntents);
const putMock = vi.mocked(putPositionIntent);

beforeEach(() => {
  listMock.mockResolvedValue(viewWith());
});

afterEach(() => {
  vi.clearAllMocks();
});

describe("PositionInvestorIntent", () => {
  it("discloses that intent is not enforced and keeps legacy lock and absence distinct", async () => {
    render(<PositionInvestorIntent portfolioId={9} />);
    expect(await screen.findByText(DISCLOSURE)).toBeTruthy();
    const pis = screen.getByLabelText("Intent for PIS.BK");
    expect(within(pis).getByText("No confirmed intent")).toBeTruthy();
    expect(within(pis).getByText("Legacy lock (meaning unconfirmed)")).toBeTruthy();
    // Legacy lock is not shown as a confirmed restriction.
    expect((within(pis).getByLabelText("Do not decrease") as HTMLInputElement).checked).toBe(false);
    expect((within(pis).getByLabelText("Do not increase") as HTMLInputElement).checked).toBe(false);
    const ptt = screen.getByLabelText("Intent for PTT.BK");
    expect(within(ptt).getByText("Confirmed · revision 2")).toBeTruthy();
    expect((within(ptt).getByLabelText("Do not decrease") as HTMLInputElement).checked).toBe(true);
    expect(putMock).not.toHaveBeenCalled();
  });

  it("shows a re-entered holding's earlier intent as needing re-confirmation and re-confirms only on click", async () => {
    const reentered = viewWith();
    reentered.positions[1] = { ...reentered.positions[1], intent_status: "RECONFIRMATION_REQUIRED" };
    listMock.mockResolvedValue(reentered);
    putMock.mockResolvedValue({ status: "RECONFIRMED", enforced_by_optimizer: false, disclosure: DISCLOSURE,
      intent: { ...confirmed, revision: 3 } });
    render(<PositionInvestorIntent portfolioId={9} />);
    const ptt = await screen.findByLabelText("Intent for PTT.BK");
    expect(within(ptt).getByText("Re-confirmation needed · revision 2 was for an earlier holding")).toBeTruthy();
    expect(within(ptt).queryByText(/^Confirmed/)).toBeNull();
    expect(putMock).not.toHaveBeenCalled();
    // Earlier values are offered for review; re-confirming needs no edit but an explicit click.
    const button = within(ptt).getByRole("button", { name: "Re-confirm intent" }) as HTMLButtonElement;
    expect(button.disabled).toBe(false);
    fireEvent.click(button);
    await waitFor(() => expect(putMock).toHaveBeenCalledWith(9, "PTT.BK", {
      increase_prohibited: false, decrease_prohibited: true, soft_preference: "PREFER_KEEP", expected_revision: 2,
    }));
    expect(await within(ptt).findByText("Confirmed · revision 3")).toBeTruthy();
  });

  it("creates intent only on explicit confirmation with a null expected revision", async () => {
    putMock.mockResolvedValue({ status: "CREATED", enforced_by_optimizer: false, disclosure: DISCLOSURE,
      intent: { ...confirmed, id: 4, position_symbol: "PIS.BK", increase_prohibited: true,
                decrease_prohibited: false, soft_preference: "NONE", revision: 1 } });
    render(<PositionInvestorIntent portfolioId={9} />);
    const pis = await screen.findByLabelText("Intent for PIS.BK");
    fireEvent.click(within(pis).getByLabelText("Do not increase"));
    fireEvent.click(within(pis).getByRole("button", { name: "Confirm intent" }));
    await waitFor(() => expect(putMock).toHaveBeenCalledWith(9, "PIS.BK", {
      increase_prohibited: true, decrease_prohibited: false, soft_preference: "NONE", expected_revision: null,
    }));
    expect(await within(pis).findByText("Confirmed · revision 1")).toBeTruthy();
  });

  it("revises with the current revision and only after a change", async () => {
    putMock.mockResolvedValue({ status: "REVISED", enforced_by_optimizer: false, disclosure: DISCLOSURE,
      intent: { ...confirmed, soft_preference: "PREFER_EXIT", revision: 3 } });
    render(<PositionInvestorIntent portfolioId={9} />);
    const ptt = await screen.findByLabelText("Intent for PTT.BK");
    const save = within(ptt).getByRole("button", { name: "Save changes" }) as HTMLButtonElement;
    expect(save.disabled).toBe(true);
    fireEvent.change(within(ptt).getByRole("combobox"), { target: { value: "PREFER_EXIT" } });
    fireEvent.click(save);
    await waitFor(() => expect(putMock).toHaveBeenCalledWith(9, "PTT.BK", {
      increase_prohibited: false, decrease_prohibited: true, soft_preference: "PREFER_EXIT", expected_revision: 2,
    }));
    expect(await within(ptt).findByText("Confirmed · revision 3")).toBeTruthy();
  });

  it("recovers from a stale revision: reloads, keeps the edit, shows saved state, saves with the new revision", async () => {
    const changedElsewhere = viewWith();
    changedElsewhere.positions[1] = { ...changedElsewhere.positions[1],
      intent: { ...confirmed, decrease_prohibited: false, soft_preference: "PREFER_EXIT", revision: 3 } };
    listMock.mockResolvedValueOnce(viewWith()).mockResolvedValueOnce(changedElsewhere);
    putMock.mockRejectedValueOnce(new Error("API 409: Intent is at revision 3; expected_revision was 2"));
    render(<PositionInvestorIntent portfolioId={9} />);
    const ptt = await screen.findByLabelText("Intent for PTT.BK");
    fireEvent.click(within(ptt).getByLabelText("Do not increase"));
    fireEvent.click(within(ptt).getByRole("button", { name: "Save changes" }));

    expect(await screen.findByText(/saved intent for PTT\.BK changed/)).toBeTruthy();
    expect(listMock).toHaveBeenCalledTimes(2);
    expect(within(ptt).getByText("Confirmed · revision 3")).toBeTruthy();
    expect(within(ptt).getByText(
      "Saved now (revision 3): Do not increase off · Do not decrease off · Prefer to exit")).toBeTruthy();
    // The owner's attempted values are kept as an unsaved draft.
    expect((within(ptt).getByLabelText("Do not increase") as HTMLInputElement).checked).toBe(true);
    expect((within(ptt).getByLabelText("Do not decrease") as HTMLInputElement).checked).toBe(true);

    putMock.mockResolvedValueOnce({ status: "REVISED", enforced_by_optimizer: false, disclosure: DISCLOSURE,
      intent: { ...confirmed, increase_prohibited: true, revision: 4 } });
    fireEvent.click(within(ptt).getByRole("button", { name: "Save changes" }));
    await waitFor(() => expect(putMock).toHaveBeenLastCalledWith(9, "PTT.BK", {
      increase_prohibited: true, decrease_prohibited: true, soft_preference: "PREFER_KEEP", expected_revision: 3,
    }));
    expect(await within(ptt).findByText("Confirmed · revision 4")).toBeTruthy();
    expect(within(ptt).queryByText(/Saved now/)).toBeNull();
  });

  it("does not resubmit a stale revision when the reload after a conflict fails", async () => {
    listMock.mockResolvedValueOnce(viewWith()).mockRejectedValueOnce(new Error("API 500: down"));
    putMock.mockRejectedValueOnce(new Error("API 409: Intent is at revision 3; expected_revision was 2"));
    render(<PositionInvestorIntent portfolioId={9} />);
    const ptt = await screen.findByLabelText("Intent for PTT.BK");
    fireEvent.click(within(ptt).getByLabelText("Do not increase"));
    fireEvent.click(within(ptt).getByRole("button", { name: "Save changes" }));
    expect(await screen.findByText(/could not be loaded\. Reload the page/)).toBeTruthy();
  });

  it("locks a row's controls while its save is in flight so a later edit is never discarded", async () => {
    let resolvePut: (value: Awaited<ReturnType<typeof putPositionIntent>>) => void = () => {};
    putMock.mockReturnValueOnce(new Promise((resolve) => { resolvePut = resolve; }));
    render(<PositionInvestorIntent portfolioId={9} />);
    const ptt = await screen.findByLabelText("Intent for PTT.BK");
    fireEvent.change(within(ptt).getByRole("combobox"), { target: { value: "PREFER_EXIT" } });
    fireEvent.click(within(ptt).getByRole("button", { name: "Save changes" }));

    const increase = within(ptt).getByLabelText("Do not increase") as HTMLInputElement;
    await waitFor(() => expect(increase.disabled).toBe(true));
    expect((within(ptt).getByLabelText("Do not decrease") as HTMLInputElement).disabled).toBe(true);
    expect((within(ptt).getByRole("combobox") as HTMLSelectElement).disabled).toBe(true);
    expect((within(ptt).getByRole("button", { name: "Save changes" }) as HTMLButtonElement).disabled).toBe(true);
    // Other rows stay editable.
    const pis = screen.getByLabelText("Intent for PIS.BK");
    expect((within(pis).getByLabelText("Do not increase") as HTMLInputElement).disabled).toBe(false);

    resolvePut({ status: "REVISED", enforced_by_optimizer: false, disclosure: DISCLOSURE,
      intent: { ...confirmed, soft_preference: "PREFER_EXIT", revision: 3 } });
    expect(await within(ptt).findByText("Confirmed · revision 3")).toBeTruthy();
    await waitFor(() => expect(increase.disabled).toBe(false));
    expect((within(ptt).getByRole("combobox") as HTMLSelectElement).value).toBe("PREFER_EXIT");
  });

  it("never lets a pending save in one portfolio leak into the same symbol in another", async () => {
    const otherPortfolio: PositionIntentView = {
      ...viewWith(), portfolio_id: 10,
      positions: [{ position_symbol: "PTT.BK", currently_held: true, holding_started_at: "2026-10-01T00:00:00", legacy_allow_swap: true,
        legacy_lock_status: null, intent_status: "CONFIRMED",
        intent: { ...confirmed, id: 30, portfolio_id: 10, decrease_prohibited: false, revision: 7 } }],
    };
    listMock.mockImplementation(async (id: number) => (id === 10 ? otherPortfolio : viewWith()));
    let resolvePut: (value: Awaited<ReturnType<typeof putPositionIntent>>) => void = () => {};
    putMock.mockReturnValueOnce(new Promise((resolve) => { resolvePut = resolve; }));

    const { rerender } = render(<PositionInvestorIntent portfolioId={9} />);
    let ptt = await screen.findByLabelText("Intent for PTT.BK");
    fireEvent.click(within(ptt).getByLabelText("Do not increase"));
    fireEvent.click(within(ptt).getByRole("button", { name: "Save changes" }));
    await waitFor(() => expect(putMock).toHaveBeenCalledTimes(1));

    rerender(<PositionInvestorIntent portfolioId={10} />);
    ptt = await screen.findByLabelText("Intent for PTT.BK");
    await within(ptt).findByText("Confirmed · revision 7");
    expect((within(ptt).getByLabelText("Do not increase") as HTMLInputElement).disabled).toBe(false);
    expect((within(ptt).getByLabelText("Do not increase") as HTMLInputElement).checked).toBe(false);

    // Portfolio 9's late success must not touch portfolio 10's row.
    resolvePut({ status: "REVISED", enforced_by_optimizer: false, disclosure: DISCLOSURE,
      intent: { ...confirmed, increase_prohibited: true, revision: 3 } });
    await waitFor(() => expect(putMock).toHaveBeenCalledTimes(1));
    await new Promise((r) => setTimeout(r, 0));
    expect(within(ptt).getByText("Confirmed · revision 7")).toBeTruthy();
    expect((within(ptt).getByLabelText("Do not increase") as HTMLInputElement).checked).toBe(false);
    expect((within(ptt).getByLabelText("Do not increase") as HTMLInputElement).disabled).toBe(false);

    // Editing and saving in portfolio 10 uses portfolio 10's own revision.
    putMock.mockResolvedValueOnce({ status: "REVISED", enforced_by_optimizer: false, disclosure: DISCLOSURE,
      intent: { ...confirmed, id: 30, portfolio_id: 10, decrease_prohibited: true, revision: 8 } });
    fireEvent.click(within(ptt).getByLabelText("Do not decrease"));
    fireEvent.click(within(ptt).getByRole("button", { name: "Save changes" }));
    await waitFor(() => expect(putMock).toHaveBeenLastCalledWith(10, "PTT.BK", {
      increase_prohibited: false, decrease_prohibited: true, soft_preference: "PREFER_KEEP", expected_revision: 7,
    }));
  });
});
