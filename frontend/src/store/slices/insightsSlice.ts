import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";

import * as insightsApi from "@/lib/api/insights";
import { getErrorMessage } from "@/lib/getErrorMessage";
import type { Insight } from "@/types";

interface InsightsState {
  items: Insight[]; // insights for the interaction currently being viewed (newest first)
  status: "idle" | "loading" | "succeeded" | "failed";
  generating: boolean; // true while a new insight is being generated
  error: string | null;
}

const initialState: InsightsState = {
  items: [],
  status: "idle",
  generating: false,
  error: null,
};

export const fetchInsights = createAsyncThunk<Insight[], number, { rejectValue: string }>(
  "insights/fetchInsights",
  async (interactionId, { rejectWithValue }) => {
    try {
      return await insightsApi.listInsights(interactionId);
    } catch (error) {
      return rejectWithValue(getErrorMessage(error));
    }
  },
);

export const generateInsight = createAsyncThunk<Insight, number, { rejectValue: string }>(
  "insights/generateInsight",
  async (interactionId, { rejectWithValue }) => {
    try {
      return await insightsApi.generateInsight(interactionId);
    } catch (error) {
      return rejectWithValue(getErrorMessage(error));
    }
  },
);

const insightsSlice = createSlice({
  name: "insights",
  initialState,
  reducers: {
    clearInsights(state) {
      state.items = [];
      state.status = "idle";
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchInsights.pending, (state) => {
        state.status = "loading";
        state.error = null;
      })
      .addCase(fetchInsights.fulfilled, (state, action) => {
        state.status = "succeeded";
        state.items = action.payload;
      })
      .addCase(fetchInsights.rejected, (state, action) => {
        state.status = "failed";
        state.error = action.payload ?? "Could not load insights.";
      });

    builder
      .addCase(generateInsight.pending, (state) => {
        state.generating = true;
      })
      .addCase(generateInsight.fulfilled, (state, action) => {
        state.generating = false;
        state.items.unshift(action.payload); // newest first
      })
      .addCase(generateInsight.rejected, (state, action) => {
        state.generating = false;
        state.error = action.payload ?? "Could not generate insight.";
      });
  },
});

export const { clearInsights } = insightsSlice.actions;
export default insightsSlice.reducer;
