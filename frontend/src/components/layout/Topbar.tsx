"use client";

import { ThemeToggle } from "@/components/theme/ThemeToggle";

export function Topbar() {
  return (
    <header className="flex h-14 items-center justify-between border-b px-4 md:px-6">
      {/* App name shows on small screens where the sidebar is hidden. */}
      <div className="font-semibold md:hidden">EngageDash</div>
      <div className="ml-auto flex items-center gap-2">
        <ThemeToggle />
      </div>
    </header>
  );
}
