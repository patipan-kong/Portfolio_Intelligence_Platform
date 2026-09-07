import { describe, test, expect, vi, beforeEach } from "vitest";
import { render, screen, fireEvent, within } from "@testing-library/react";
import { PortfolioProvider } from "@/lib/PortfolioContext";
import Navbar from "@/components/Navbar";
import { NAV_GROUPS } from "@/lib/navigationConfig";

// Wealth OS Navigation IA milestone — behavioral coverage for the grouped
// desktop dropdowns and grouped mobile drawer, both rendered from the same
// NAV_GROUPS config (frontend/lib/navigationConfig.ts).

const { listPortfolios, createPortfolio, deletePortfolio, getSystemStatus } = vi.hoisted(() => ({
  listPortfolios: vi.fn(),
  createPortfolio: vi.fn(),
  deletePortfolio: vi.fn(),
  getSystemStatus: vi.fn(),
}));

vi.mock("@/lib/api", () => ({
  listPortfolios,
  createPortfolio,
  deletePortfolio,
  getSystemStatus,
}));

const { usePathname } = vi.hoisted(() => ({ usePathname: vi.fn(() => "/portfolio") }));
vi.mock("next/navigation", () => ({ usePathname }));

beforeEach(() => {
  localStorage.clear();
  listPortfolios.mockReset().mockResolvedValue([]);
  getSystemStatus.mockReset().mockResolvedValue({ read_only_market_data: false });
  usePathname.mockReturnValue("/portfolio");
});

function renderNavbar() {
  return render(
    <PortfolioProvider>
      <Navbar />
    </PortfolioProvider>
  );
}

const GROUP_LABELS = NAV_GROUPS.map((g) => g.label);
const investments = NAV_GROUPS.find((g) => g.key === "investments")!;
const wealth = NAV_GROUPS.find((g) => g.key === "wealth")!;
const planning = NAV_GROUPS.find((g) => g.key === "planning")!;
const ai = NAV_GROUPS.find((g) => g.key === "ai")!;

function desktopTrigger(label: string) {
  // Anchored: "ระบบ" (System) must not match "ออกจากระบบ" (Logout).
  return screen.getByRole("button", { name: new RegExp(`^${label}`) });
}

/** Labels of the menu items in the currently open dropdown that render active. */
function activeMenuItems(): (string | null)[] {
  return within(screen.getByRole("menu"))
    .getAllByRole("menuitem")
    .filter((el) => el.className.includes("bg-blue-50"))
    .map((el) => el.textContent);
}

/** A group's drawer section header (last match — the desktop trigger is first). */
function mobileHeader(label: string) {
  const found = screen.getAllByRole("button", { name: new RegExp(`^${label}`) });
  return found[found.length - 1];
}

describe("Navbar — desktop grouped navigation", () => {
  test("the approved groups render as top-level triggers", () => {
    renderNavbar();
    for (const label of GROUP_LABELS) {
      expect(screen.getByRole("button", { name: new RegExp(`^${label}`) })).toBeInTheDocument();
    }
  });

  test("the old flat 9-link structure is gone: leaf labels are not top-level buttons", () => {
    renderNavbar();
    // Leaf items only exist inside a closed dropdown's menu, not as their own
    // top-level trigger button (which is what the pre-IA flat nav rendered).
    expect(screen.queryByRole("button", { name: "พอร์ตโฟลิโอ" })).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "รายการเฝ้าดู" })).not.toBeInTheDocument();
    expect(screen.queryByRole("button", { name: "Cash Flow" })).not.toBeInTheDocument();
    expect(screen.queryByRole("menuitem")).not.toBeInTheDocument(); // nothing open yet
  });

  test("Watchlist belongs to the Investments group", () => {
    renderNavbar();
    fireEvent.click(desktopTrigger(investments.label));
    const menu = screen.getByRole("menu");
    expect(within(menu).getByText("รายการเฝ้าดู")).toBeInTheDocument();
    expect(within(menu).getByText("พอร์ตโฟลิโอ")).toBeInTheDocument();
  });

  test("both AI destinations belong to the AI group", () => {
    renderNavbar();
    fireEvent.click(desktopTrigger(ai.label));
    const menu = screen.getByRole("menu");
    expect(within(menu).getByText("ศูนย์บัญชาการ AI")).toBeInTheDocument();
    expect(within(menu).getByText("ประเมินผล AI")).toBeInTheDocument();
  });

  test("a direct route activates only its owning group", () => {
    usePathname.mockReturnValue("/cash");
    renderNavbar();
    expect(desktopTrigger(wealth.label)).toHaveClass("bg-blue-50");
    expect(desktopTrigger(investments.label)).not.toHaveClass("bg-blue-50");
    expect(desktopTrigger(planning.label)).not.toHaveClass("bg-blue-50");
  });

  test("/cash-flow is owned by the Cash Flow leaf, not by the /cash leaf", () => {
    // Leaf-level proof of the segment-boundary fix in isActive(). Both leaves
    // live in the same Wealth group, so a group-level assertion cannot tell
    // them apart — under the old raw startsWith(), /cash-flow lit up both.
    usePathname.mockReturnValue("/cash-flow");
    renderNavbar();
    expect(desktopTrigger(wealth.label)).toHaveClass("bg-blue-50");

    fireEvent.click(desktopTrigger(wealth.label));
    expect(activeMenuItems()).toEqual(["Cash Flow"]);
  });

  test("a dynamic/detail route activates its owning group", () => {
    usePathname.mockReturnValue("/goals/123");
    renderNavbar();
    expect(desktopTrigger(planning.label)).toHaveClass("bg-blue-50");
  });

  test("Portfolio secondary routes (owned by PortfolioTabs) activate Investments", () => {
    usePathname.mockReturnValue("/performance");
    renderNavbar();
    expect(desktopTrigger(investments.label)).toHaveClass("bg-blue-50");
  });

  test("optimizer and portfolio-intelligence activate AI without becoming nav leaves", () => {
    usePathname.mockReturnValue("/optimizer");
    renderNavbar();
    expect(desktopTrigger(ai.label)).toHaveClass("bg-blue-50");
    expect(screen.queryByText("Optimizer")).not.toBeInTheDocument();
    fireEvent.click(desktopTrigger(ai.label));
    // The AI menu exposes only the two approved leaves, not /optimizer itself.
    const menu = screen.getByRole("menu");
    expect(within(menu).getAllByRole("menuitem")).toHaveLength(2);
  });

  test("/portfolio-intelligence activates AI and never the /portfolio leaf", () => {
    // The named counterexample: the "/portfolio" prefix must not swallow
    // "/portfolio-intelligence", which belongs to the AI group.
    usePathname.mockReturnValue("/portfolio-intelligence");
    renderNavbar();
    expect(desktopTrigger(ai.label)).toHaveClass("bg-blue-50");
    expect(desktopTrigger(investments.label)).not.toHaveClass("bg-blue-50");

    fireEvent.click(desktopTrigger(investments.label));
    expect(activeMenuItems()).toEqual([]);
  });

  test("a group opens on click and closes on a second click", () => {
    renderNavbar();
    const trigger = desktopTrigger(investments.label);
    expect(screen.queryByRole("menu")).not.toBeInTheDocument();
    fireEvent.click(trigger);
    expect(screen.getByRole("menu")).toBeInTheDocument();
    fireEvent.click(trigger);
    expect(screen.queryByRole("menu")).not.toBeInTheDocument();
  });

  test("only one group is open at a time", () => {
    renderNavbar();
    fireEvent.click(desktopTrigger(investments.label));
    fireEvent.click(desktopTrigger(wealth.label));

    const menus = screen.getAllByRole("menu");
    expect(menus).toHaveLength(1);
    expect(within(menus[0]).getAllByRole("menuitem").map((el) => el.textContent)).toEqual(
      wealth.items.map((item) => item.label)
    );
    expect(desktopTrigger(investments.label)).toHaveAttribute("aria-expanded", "false");
    expect(desktopTrigger(wealth.label)).toHaveAttribute("aria-expanded", "true");
  });

  test("a route change closes a stale open dropdown", () => {
    const { rerender } = renderNavbar();
    fireEvent.click(desktopTrigger(investments.label));
    expect(screen.getByRole("menu")).toBeInTheDocument();

    usePathname.mockReturnValue("/goals");
    rerender(
      <PortfolioProvider>
        <Navbar />
      </PortfolioProvider>
    );
    expect(screen.queryByRole("menu")).not.toBeInTheDocument();
    expect(desktopTrigger(investments.label)).toHaveAttribute("aria-expanded", "false");
  });

  test("an outside click closes the open group", () => {
    renderNavbar();
    fireEvent.click(desktopTrigger(investments.label));
    expect(screen.getByRole("menu")).toBeInTheDocument();
    fireEvent.mouseDown(document.body);
    expect(screen.queryByRole("menu")).not.toBeInTheDocument();
  });

  test("Escape closes the open group and returns focus to its trigger", () => {
    renderNavbar();
    const trigger = desktopTrigger(investments.label);
    fireEvent.click(trigger);
    expect(screen.getByRole("menu")).toBeInTheDocument();
    fireEvent.keyDown(document, { key: "Escape" });
    expect(screen.queryByRole("menu")).not.toBeInTheDocument();
    expect(document.activeElement).toBe(trigger);
  });

  test("aria-expanded tracks the open/closed state", () => {
    renderNavbar();
    const trigger = desktopTrigger(investments.label);
    expect(trigger).toHaveAttribute("aria-expanded", "false");
    fireEvent.click(trigger);
    expect(trigger).toHaveAttribute("aria-expanded", "true");
    fireEvent.click(trigger);
    expect(trigger).toHaveAttribute("aria-expanded", "false");
  });
});

describe("Navbar — mobile grouped drawer", () => {
  test("the hamburger opens and closes the drawer", () => {
    renderNavbar();
    const hamburger = screen.getByLabelText("Toggle menu");
    const groupNamePattern = new RegExp(`^${wealth.label}`);

    // Closed: only the desktop trigger matches the group label.
    expect(screen.getAllByRole("button", { name: groupNamePattern })).toHaveLength(1);

    fireEvent.click(hamburger);
    // Open: the mobile drawer's own section header now also matches.
    expect(screen.getAllByRole("button", { name: groupNamePattern })).toHaveLength(2);

    fireEvent.click(hamburger);
    expect(screen.getAllByRole("button", { name: groupNamePattern })).toHaveLength(1);
  });

  test("mobile groups expand and collapse independently of the desktop menu", () => {
    renderNavbar();
    fireEvent.click(screen.getByLabelText("Toggle menu"));
    const mobileTriggers = screen.getAllByRole("button", { name: new RegExp(`^${wealth.label}`) });
    const mobileHeader = mobileTriggers[mobileTriggers.length - 1];
    expect(mobileHeader).toHaveAttribute("aria-expanded", "false");
    fireEvent.click(mobileHeader);
    expect(mobileHeader).toHaveAttribute("aria-expanded", "true");
    expect(screen.getByText("Liabilities")).toBeInTheDocument();
    fireEvent.click(mobileHeader);
    expect(mobileHeader).toHaveAttribute("aria-expanded", "false");
  });

  test("only one mobile group expands at a time", () => {
    renderNavbar();
    fireEvent.click(screen.getByLabelText("Toggle menu"));
    // "/portfolio" is the default mocked route, so Investments starts expanded.
    expect(mobileHeader(investments.label)).toHaveAttribute("aria-expanded", "true");

    fireEvent.click(mobileHeader(wealth.label));
    expect(mobileHeader(wealth.label)).toHaveAttribute("aria-expanded", "true");
    expect(mobileHeader(investments.label)).toHaveAttribute("aria-expanded", "false");
  });

  test("the group owning the current route starts expanded in the drawer", () => {
    usePathname.mockReturnValue("/goals");
    renderNavbar();
    fireEvent.click(screen.getByLabelText("Toggle menu"));
    const planningHeaders = screen.getAllByRole("button", { name: new RegExp(`^${planning.label}`) });
    const mobileHeader = planningHeaders[planningHeaders.length - 1];
    expect(mobileHeader).toHaveAttribute("aria-expanded", "true");
    // A group with no owned route active starts collapsed.
    const wealthHeaders = screen.getAllByRole("button", { name: new RegExp(`^${wealth.label}`) });
    expect(wealthHeaders[wealthHeaders.length - 1]).toHaveAttribute("aria-expanded", "false");
  });

  test("a route change closes the mobile drawer", () => {
    const { rerender } = renderNavbar();
    fireEvent.click(screen.getByLabelText("Toggle menu"));
    expect(screen.getByLabelText("Toggle menu")).toHaveAttribute("aria-expanded", "true");
    usePathname.mockReturnValue("/cash");
    rerender(
      <PortfolioProvider>
        <Navbar />
      </PortfolioProvider>
    );
    expect(screen.getByLabelText("Toggle menu")).toHaveAttribute("aria-expanded", "false");
  });
});

describe("Navbar — shared config", () => {
  test("desktop and mobile render the same group ownership from NAV_GROUPS", () => {
    renderNavbar();
    for (const group of NAV_GROUPS) {
      fireEvent.click(desktopTrigger(group.label));
      const menu = screen.getByRole("menu");
      const desktopItemLabels = within(menu)
        .getAllByRole("menuitem")
        .map((el) => el.textContent);
      fireEvent.click(desktopTrigger(group.label)); // close before opening the next

      expect(desktopItemLabels).toEqual(group.items.map((item) => item.label));
    }

    fireEvent.click(screen.getByLabelText("Toggle menu"));
    for (const group of NAV_GROUPS) {
      const headers = screen.getAllByRole("button", { name: new RegExp(`^${group.label}`) });
      const mobileHeader = headers[headers.length - 1];
      // The route-owning group (Investments, for the default mocked "/portfolio")
      // starts expanded already — only click groups that start collapsed.
      if (mobileHeader.getAttribute("aria-expanded") === "false") {
        fireEvent.click(mobileHeader);
      }
      for (const item of group.items) {
        expect(screen.getAllByText(item.label).length).toBeGreaterThan(0);
      }
    }
  });
});
