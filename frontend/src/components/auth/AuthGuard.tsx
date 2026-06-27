"use client";

import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { getAccessToken } from "@/lib/tokenStorage";

/**
 * Protects the app pages: if there is no access token, send the user to /login.
 *
 * This is the scaffolding version (checks the token in localStorage). In Phase 8
 * it is hooked into the Redux auth state so it also reacts to login/logout.
 */
export function AuthGuard({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const [allowed, setAllowed] = useState(false);

  useEffect(() => {
    // We can only read localStorage on the client, so the auth check runs on mount.
    if (getAccessToken()) {
      // eslint-disable-next-line react-hooks/set-state-in-effect -- on-mount auth check
      setAllowed(true);
    } else {
      router.replace("/login");
    }
  }, [router]);

  // Render nothing until we know the user is allowed (avoids flashing the page).
  if (!allowed) return null;

  return <>{children}</>;
}
