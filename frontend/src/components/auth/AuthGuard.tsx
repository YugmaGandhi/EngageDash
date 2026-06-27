"use client";

import { useRouter } from "next/navigation";
import { useEffect } from "react";

import { Loading } from "@/components/common/Loading";
import { getAccessToken } from "@/lib/tokenStorage";
import { useAppSelector } from "@/store/hooks";

/**
 * Protects the app pages.
 *
 * - No token at all -> redirect to /login.
 * - Token present but profile not loaded yet -> show a loading spinner.
 * - Authenticated -> render the page.
 * - Token rejected (status "unauthenticated") -> redirect to /login.
 */
export function AuthGuard({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const status = useAppSelector((s) => s.auth.status);

  useEffect(() => {
    if (!getAccessToken()) {
      router.replace("/login");
    }
  }, [router]);

  useEffect(() => {
    if (status === "unauthenticated") {
      router.replace("/login");
    }
  }, [status, router]);

  if (status === "authenticated") {
    return <>{children}</>;
  }

  // Either loading the profile, or about to redirect.
  return <Loading label="Loading..." />;
}
