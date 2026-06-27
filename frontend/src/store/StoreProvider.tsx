"use client";

import { Provider } from "react-redux";

import { AuthInitializer } from "@/components/auth/AuthInitializer";

import { store } from "./store";

// Wraps the app so any component can use the Redux store.
// This must be a client component (Redux runs in the browser).
// AuthInitializer restores the logged-in session on load.
export function StoreProvider({ children }: { children: React.ReactNode }) {
  return (
    <Provider store={store}>
      <AuthInitializer>{children}</AuthInitializer>
    </Provider>
  );
}
