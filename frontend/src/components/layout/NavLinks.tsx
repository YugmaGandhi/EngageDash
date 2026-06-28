"use client";

import { LayoutDashboard, MessagesSquare, Shield, Users } from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";

import { cn } from "@/lib/utils";
import { useAppSelector } from "@/store/hooks";

const baseNavItems = [
  { href: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { href: "/customers", label: "Customers", icon: Users },
  { href: "/interactions", label: "Interactions", icon: MessagesSquare },
];

// The navigation links, shared by the desktop sidebar and the mobile drawer.
// `onNavigate` lets the mobile drawer close itself when a link is tapped.
export function NavLinks({ onNavigate }: { onNavigate?: () => void }) {
  const pathname = usePathname();
  const role = useAppSelector((s) => s.auth.user?.role);

  // Only admins see the Users management link.
  const navItems =
    role === "admin"
      ? [...baseNavItems, { href: "/users", label: "Users", icon: Shield }]
      : baseNavItems;

  return (
    <nav className="space-y-1 px-3">
      {navItems.map(({ href, label, icon: Icon }) => {
        const active = pathname.startsWith(href);
        return (
          <Link
            key={href}
            href={href}
            onClick={onNavigate}
            className={cn(
              "flex items-center gap-3 rounded-md px-3 py-2 text-sm transition-colors",
              active
                ? "bg-accent text-accent-foreground font-medium"
                : "text-muted-foreground hover:bg-accent hover:text-accent-foreground",
            )}
          >
            <Icon className="h-4 w-4" />
            {label}
          </Link>
        );
      })}
    </nav>
  );
}
