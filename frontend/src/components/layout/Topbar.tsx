"use client";

import { LogOut } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";

import { ThemeToggle } from "@/components/theme/ThemeToggle";
import { Button } from "@/components/ui/button";
import { useAppDispatch, useAppSelector } from "@/store/hooks";
import { logout } from "@/store/slices/authSlice";

export function Topbar() {
  const user = useAppSelector((s) => s.auth.user);
  const dispatch = useAppDispatch();
  const router = useRouter();

  function handleLogout() {
    dispatch(logout());
    router.replace("/login");
  }

  return (
    <header className="flex h-14 items-center justify-between border-b px-4 md:px-6">
      {/* App name shows on small screens where the sidebar is hidden. */}
      <div className="font-semibold md:hidden">EngageDash</div>
      <div className="ml-auto flex items-center gap-3">
        {user && (
          <Link href="/profile" className="text-sm hover:underline">
            {user.name}
          </Link>
        )}
        <ThemeToggle />
        <Button variant="ghost" size="icon" onClick={handleLogout} aria-label="Log out">
          <LogOut className="h-5 w-5" />
        </Button>
      </div>
    </header>
  );
}
