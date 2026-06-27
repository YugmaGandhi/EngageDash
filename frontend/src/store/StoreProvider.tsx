"use client";

import { Provider } from "react-redux";

import { store } from "./store";

// Wraps the app so any component can use the Redux store.
// This must be a client component (Redux runs in the browser).
export function StoreProvider({ children }: { children: React.ReactNode }) {
  return <Provider store={store}>{children}</Provider>;
}
