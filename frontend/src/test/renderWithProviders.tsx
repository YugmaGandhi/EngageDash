import { configureStore } from "@reduxjs/toolkit";
import { render } from "@testing-library/react";
import type { ReactElement } from "react";
import { Provider } from "react-redux";

import authReducer, { type AuthState } from "@/store/slices/authSlice";
import customersReducer from "@/store/slices/customersSlice";
import dashboardReducer from "@/store/slices/dashboardSlice";
import insightsReducer from "@/store/slices/insightsSlice";
import interactionsReducer from "@/store/slices/interactionsSlice";

// Build a fresh store for a test, optionally with preloaded auth state.
export function makeTestStore(auth?: AuthState) {
  return configureStore({
    reducer: {
      auth: authReducer,
      customers: customersReducer,
      interactions: interactionsReducer,
      insights: insightsReducer,
      dashboard: dashboardReducer,
    },
    preloadedState: auth ? { auth } : undefined,
  });
}

// Render a component wrapped in a Redux provider (so hooks like useAppSelector work).
export function renderWithProviders(ui: ReactElement, options?: { auth?: AuthState }) {
  const store = makeTestStore(options?.auth);
  return { store, ...render(<Provider store={store}>{ui}</Provider>) };
}
