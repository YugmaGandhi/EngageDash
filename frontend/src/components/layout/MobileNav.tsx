"use client";

import { Menu, X } from "lucide-react";
import { useState } from "react";

import { Button } from "@/components/ui/button";

import { NavLinks } from "./NavLinks";

// Hamburger menu + slide-in drawer for small screens (the sidebar is hidden there).
export function MobileNav() {
  const [open, setOpen] = useState(false);

  return (
    <div className="md:hidden">
      <Button variant="ghost" size="icon" onClick={() => setOpen(true)} aria-label="Open menu">
        <Menu className="h-5 w-5" />
      </Button>

      {open && (
        <div className="fixed inset-0 z-50">
          {/* Dim the page; tapping it closes the drawer. */}
          <div className="absolute inset-0 bg-black/50" onClick={() => setOpen(false)} />
          <aside className="bg-sidebar absolute top-0 left-0 h-full w-64 border-r shadow-lg">
            <div className="flex h-14 items-center justify-between px-6">
              <span className="text-lg font-bold">EngageDash</span>
              <Button
                variant="ghost"
                size="icon"
                onClick={() => setOpen(false)}
                aria-label="Close menu"
              >
                <X className="h-5 w-5" />
              </Button>
            </div>
            <NavLinks onNavigate={() => setOpen(false)} />
          </aside>
        </div>
      )}
    </div>
  );
}
