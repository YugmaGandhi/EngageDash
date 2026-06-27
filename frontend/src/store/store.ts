import { configureStore } from "@reduxjs/toolkit";

import authReducer from "./slices/authSlice";
import customersReducer from "./slices/customersSlice";
import interactionsReducer from "./slices/interactionsSlice";

export const store = configureStore({
  reducer: {
    auth: authReducer,
    customers: customersReducer,
    interactions: interactionsReducer,
    // The dashboard slice is added in Phase 10.
  },
});

// Types inferred from the store itself, used by the typed hooks.
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
