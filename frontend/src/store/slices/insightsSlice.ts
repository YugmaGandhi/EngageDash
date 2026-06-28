import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";

import * as insightsApi from "@/lib/api/insights";
import { getErrorMessage } from "@/lib/getErrorMessage";
import type { Insight } from "@/types";

interface InsightsState {
  items: Insight[]; // insights for the interaction currently being viewed (newest first)
  status: "idle" | "loading" | "succeeded" | "failed";
  currentInteractionId: number | null; // which interaction `items` belong to
  // Which interaction is currently generating (null = none). Only one runs at a
  // time, so this doubles as the "is anything generating" flag.
  generatingId: number | null;
  generatingTitle: string | null; // its title, so any page can name it
  error: string | null;
}

const initialState: InsightsState = {
  items: [],
  status: "idle",
  currentInteractionId: null,
  generatingId: null,
  generatingTitle: null,
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

// We pass the title too (not just the id) so any screen can show which
// interaction is currently being generated.
export const generateInsight = createAsyncThunk<
  Insight,
  { id: number; title: string },
  { rejectValue: string }
>("insights/generateInsight", async ({ id }, { rejectWithValue }) => {
  try {
    return await insightsApi.generateInsight(id);
  } catch (error) {
    return rejectWithValue(getErrorMessage(error));
  }
});

const insightsSlice = createSlice({
  name: "insights",
  initialState,
  reducers: {
    clearInsights(state) {
      state.items = [];
      state.status = "idle";
      state.currentInteractionId = null;
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchInsights.pending, (state, action) => {
        state.status = "loading";
        state.currentInteractionId = action.meta.arg; // the interaction we're loading
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
      .addCase(generateInsight.pending, (state, action) => {
        state.generatingId = action.meta.arg.id;
        state.generatingTitle = action.meta.arg.title;
      })
      .addCase(generateInsight.fulfilled, (state, action) => {
        state.generatingId = null;
        state.generatingTitle = null;
        // Only add it to the visible list if the user is still on that
        // interaction; otherwise it loads when they open that interaction.
        if (action.payload.interaction_id === state.currentInteractionId) {
          state.items.unshift(action.payload); // newest first
        }
      })
      .addCase(generateInsight.rejected, (state, action) => {
        state.generatingId = null;
        state.generatingTitle = null;
        state.error = action.payload ?? "Could not generate insight.";
      });
  },
});

export const { clearInsights } = insightsSlice.actions;
export default insightsSlice.reducer;
