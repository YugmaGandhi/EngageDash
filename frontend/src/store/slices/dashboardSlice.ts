import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";

import { getDashboard } from "@/lib/api/dashboard";
import { getErrorMessage } from "@/lib/getErrorMessage";
import type { DashboardData } from "@/types";

interface DashboardState {
  data: DashboardData | null;
  status: "idle" | "loading" | "succeeded" | "failed";
  error: string | null;
}

const initialState: DashboardState = {
  data: null,
  status: "idle",
  error: null,
};

export const fetchDashboard = createAsyncThunk<DashboardData, void, { rejectValue: string }>(
  "dashboard/fetchDashboard",
  async (_, { rejectWithValue }) => {
    try {
      return await getDashboard();
    } catch (error) {
      return rejectWithValue(getErrorMessage(error));
    }
  },
);

const dashboardSlice = createSlice({
  name: "dashboard",
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchDashboard.pending, (state) => {
        state.status = "loading";
        state.error = null;
      })
      .addCase(fetchDashboard.fulfilled, (state, action) => {
        state.status = "succeeded";
        state.data = action.payload;
      })
      .addCase(fetchDashboard.rejected, (state, action) => {
        state.status = "failed";
        state.error = action.payload ?? "Could not load the dashboard.";
      });
  },
});

export default dashboardSlice.reducer;
