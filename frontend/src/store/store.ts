import { configureStore } from "@reduxjs/toolkit";

export const store = configureStore({
  reducer: {
    // Feature slices (auth, customers, interactions, dashboard) are added in
    // later phases. This small placeholder keeps the store valid until then.
    app: (state: { ready: boolean } = { ready: true }) => state,
  },
});

// Types inferred from the store itself, used by the typed hooks.
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
