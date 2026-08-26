"use client";

import { useState, useEffect, useRef } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { logout } from "@/lib/auth";
import { usePortfolio } from "@/lib/PortfolioContext";
import { getSystemStatus, type SystemStatus } from "@/lib/api";
import WorkspaceScopeSwitcher from "@/components/WorkspaceScopeSwitcher";
import { NAV_GROUPS, isActive, isGroupActive } from "@/lib/navigationConfig";

export default function Navbar() {
  const pathname = usePathname();
  const { portfolios } = usePortfolio();
  const [openGroup, setOpenGroup] = useState<string | null>(null);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [mobileExpanded, setMobileExpanded] = useState<string | null>(null);
  const [sysStatus, setSysStatus] = useState<SystemStatus | null>(null);
  const groupRefs = useRef<Record<string, HTMLDivElement | null>>({});
  const triggerRefs = useRef<Record<string, HTMLButtonElement | null>>({});

  useEffect(() => {
    getSystemStatus()
      .then(setSysStatus)
      .catch(() => {});
  }, []);

  // Close the open desktop dropdown on outside click.
  useEffect(() => {
    function onMouseDown(e: MouseEvent) {
      if (!openGroup) return;
      const container = groupRefs.current[openGroup];
      if (container && !container.contains(e.target as Node)) {
        setOpenGroup(null);
      }
    }
    document.addEventListener("mousedown", onMouseDown);
    return () => document.removeEventListener("mousedown", onMouseDown);
  }, [openGroup]);

  // Escape closes the open dropdown and returns focus to its trigger.
  useEffect(() => {
    function onKeyDown(e: KeyboardEvent) {
      if (e.key !== "Escape" || !openGroup) return;
      const key = openGroup;
      setOpenGroup(null);
      triggerRefs.current[key]?.focus();
    }
    document.addEventListener("keydown", onKeyDown);
    return () => document.removeEventListener("keydown", onKeyDown);
  }, [openGroup]);

  // Close everything on route change.
  useEffect(() => {
    setOpenGroup(null);
    setMobileOpen(false);
  }, [pathname]);

  // Mobile drawer: the group owning the current route starts expanded; the
  // rest start collapsed. Recomputed whenever the route or drawer changes.
  useEffect(() => {
    const active = NAV_GROUPS.find((group) => isGroupActive(group, pathname));
    setMobileExpanded(active ? active.key : null);
  }, [pathname, mobileOpen]);

  return (
    <nav className="bg-white border-b px-4 py-2.5">
      {/* ── Desktop row ── */}
      <div className="max-w-5xl mx-auto flex items-center gap-2">

        {/* Brand — links to the legacy dashboard (route kept; removed from nav) */}
        <Link
          href="/"
          className="text-sm font-bold text-gray-800 shrink-0 mr-4 hover:text-blue-700 transition-colors"
        >
          📈 Portfolio Intelligence
        </Link>

        {/* Cloud Dashboard Mode badge — shown only when APP_ENV=vps */}
        {sysStatus?.read_only_market_data && (
          <span
            title="Market data synced from Local Research Node. Live fetching disabled."
            className="hidden md:inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs font-medium bg-sky-50 text-sky-700 border border-sky-200 shrink-0 mr-1"
          >
            ☁ Cloud Dashboard
          </span>
        )}

        {/* Main nav — grouped dropdowns */}
        <div className="hidden md:flex items-center gap-1">
          {NAV_GROUPS.map((group) => {
            const active = isGroupActive(group, pathname);
            const open = openGroup === group.key;
            return (
              <div
                key={group.key}
                className="relative"
                ref={(el) => {
                  groupRefs.current[group.key] = el;
                }}
              >
                <button
                  ref={(el) => {
                    triggerRefs.current[group.key] = el;
                  }}
                  onClick={() => setOpenGroup((k) => (k === group.key ? null : group.key))}
                  aria-expanded={open}
                  aria-haspopup="menu"
                  className={`flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg text-sm font-medium transition-colors whitespace-nowrap ${
                    active
                      ? "bg-blue-50 text-blue-700"
                      : "text-gray-600 hover:bg-gray-100 hover:text-gray-800"
                  }`}
                >
                  <span>{group.label}</span>
                  <span className="text-xs text-gray-400">{open ? "▲" : "▼"}</span>
                </button>

                {open && (
                  <div
                    role="menu"
                    className="absolute left-0 mt-1.5 w-52 bg-white border border-gray-200 rounded-xl shadow-lg py-1.5 z-50"
                  >
                    {group.items.map((item) => (
                      <Link
                        key={item.href}
                        href={item.href}
                        role="menuitem"
                        className={`flex items-center px-4 py-2 text-sm transition-colors ${
                          isActive(item.match, pathname)
                            ? "bg-blue-50 text-blue-700 font-medium"
                            : "text-gray-700 hover:bg-gray-50"
                        }`}
                      >
                        {item.label}
                      </Link>
                    ))}
                  </div>
                )}
              </div>
            );
          })}
        </div>

        {/* Push switcher + logout to the right */}
        <div className="hidden md:flex items-center gap-2 ml-auto">

          {/* Portfolio selector — M36.1 Phase 3 shared Workspace-Scope contract */}
          <WorkspaceScopeSwitcher variant="dropdown" label="เลือกพอร์ต" noneLabel="ไม่ได้เลือกพอร์ต" />

          {/* Logout */}
          <button
            onClick={logout}
            className="text-sm text-gray-400 hover:text-gray-600 border rounded px-2.5 py-1 hover:bg-gray-50"
          >
            ออกจากระบบ
          </button>
        </div>

        {/* Hamburger — mobile only */}
        <button
          onClick={() => setMobileOpen((o) => !o)}
          className="md:hidden ml-auto p-1.5 rounded-md text-gray-500 hover:bg-gray-100 text-base leading-none"
          aria-label="Toggle menu"
          aria-expanded={mobileOpen}
        >
          {mobileOpen ? "✕" : "☰"}
        </button>
      </div>

      {/* ── Mobile panel — same grouped ownership as desktop ── */}
      {mobileOpen && (
        <div className="md:hidden mt-2 border-t pt-2 pb-2 space-y-1">
          {NAV_GROUPS.map((group) => {
            const active = isGroupActive(group, pathname);
            const expanded = mobileExpanded === group.key;
            return (
              <div key={group.key} className="border-b last:border-b-0">
                <button
                  onClick={() => setMobileExpanded((k) => (k === group.key ? null : group.key))}
                  aria-expanded={expanded}
                  className={`w-full flex items-center justify-between px-3 py-2 text-sm font-semibold transition-colors ${
                    active ? "text-blue-700" : "text-gray-700"
                  }`}
                >
                  <span>{group.label}</span>
                  <span className="text-xs text-gray-400">{expanded ? "▲" : "▼"}</span>
                </button>

                {expanded && (
                  <div className="pl-2 pb-2 space-y-0.5">
                    {group.items.map((item) => (
                      <Link
                        key={item.href}
                        href={item.href}
                        className={`block px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                          isActive(item.match, pathname)
                            ? "bg-blue-50 text-blue-700"
                            : "text-gray-600 hover:bg-gray-100"
                        }`}
                      >
                        {item.label}
                      </Link>
                    ))}
                  </div>
                )}
              </div>
            );
          })}

          {portfolios.length > 0 && (
            <>
              <div className="my-2 border-t" />
              <p className="px-3 pb-1 text-xs font-semibold text-gray-400 uppercase tracking-wider">เลือกพอร์ต</p>
              <WorkspaceScopeSwitcher variant="list" noneLabel="ไม่ได้เลือกพอร์ต" className="space-y-0.5" />
            </>
          )}

          <div className="my-2 border-t" />

          <button
            onClick={logout}
            className="w-full text-left px-3 py-2 rounded-md text-sm text-gray-400 hover:text-gray-600 hover:bg-gray-50"
          >
            ออกจากระบบ
          </button>
        </div>
      )}
    </nav>
  );
}
