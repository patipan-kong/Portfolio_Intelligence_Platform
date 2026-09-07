// Shared navigation ownership — desktop grouped dropdowns and the mobile
// drawer both render from this single config (Wealth OS Navigation IA
// milestone). Child/detail routes must never appear here directly; they
// inherit their owning leaf's `match` prefix instead (e.g. /goals/[id] is
// owned by the Goals leaf via "/goals", /stock/[symbol] via "/portfolio"'s
// "/stock" prefix).

export interface NavLeaf {
  label: string;
  href: string;
  /** Route prefixes owned by this leaf, including its own child/detail routes. */
  match: string[];
}

export interface NavGroup {
  key: string;
  label: string;
  items: NavLeaf[];
}

export const NAV_GROUPS: NavGroup[] = [
  {
    key: "investments",
    label: "การลงทุน",
    items: [
      {
        label: "พอร์ตโฟลิโอ",
        href: "/portfolio",
        // /performance, /analytics, /history, /income, /import stay owned by
        // this leaf — PortfolioTabs.tsx remains their sub-nav, unchanged.
        match: ["/portfolio", "/performance", "/analytics", "/history", "/income", "/import", "/stock"],
      },
      { label: "รายการเฝ้าดู", href: "/watchlist", match: ["/watchlist"] },
    ],
  },
  {
    key: "wealth",
    label: "ความมั่งคั่ง",
    items: [
      { label: "บัญชีเงินสด", href: "/cash", match: ["/cash"] },
      { label: "Cash Flow", href: "/cash-flow", match: ["/cash-flow"] },
      { label: "Liabilities", href: "/liabilities", match: ["/liabilities"] },
    ],
  },
  {
    key: "planning",
    label: "การวางแผน",
    items: [{ label: "Goals", href: "/goals", match: ["/goals"] }],
  },
  {
    key: "ai",
    label: "AI",
    items: [
      {
        label: "ศูนย์บัญชาการ AI",
        href: "/operations-center",
        match: ["/operations-center", "/optimizer", "/portfolio-intelligence"],
      },
      { label: "ประเมินผล AI", href: "/ai-analytics", match: ["/ai-analytics"] },
    ],
  },
  {
    key: "system",
    label: "ระบบ",
    items: [
      { label: "📚 คู่มือ", href: "/system-guide", match: ["/system-guide"] },
      { label: "ตั้งค่า", href: "/settings", match: ["/settings"] },
    ],
  },
];

/**
 * Segment-boundary prefix match: "/cash" must not match "/cash-flow", and
 * "/portfolio" must not match "/portfolio-intelligence".
 */
export function isActive(match: string[], pathname: string): boolean {
  return match.some((prefix) =>
    prefix === "/" ? pathname === "/" : pathname === prefix || pathname.startsWith(prefix + "/")
  );
}

export function isGroupActive(group: NavGroup, pathname: string): boolean {
  return group.items.some((item) => isActive(item.match, pathname));
}
