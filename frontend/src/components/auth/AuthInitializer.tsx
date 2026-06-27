"use client";

import { useEffect } from "react";

import { getAccessToken } from "@/lib/tokenStorage";
import { useAppDispatch } from "@/store/hooks";
import { fetchProfile } from "@/store/slices/authSlice";

/**
 * On first load, if a token is saved, fetch the user's profile so the session is
 * restored after a refresh (the user stays logged in).
 */
export function AuthInitializer({ children }: { children: React.ReactNode }) {
  const dispatch = useAppDispatch();

  useEffect(() => {
    if (getAccessToken()) {
      dispatch(fetchProfile());
    }
  }, [dispatch]);

  return <>{children}</>;
}
