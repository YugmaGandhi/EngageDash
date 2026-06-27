import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";

import * as interactionsApi from "@/lib/api/interactions";
import { getErrorMessage } from "@/lib/getErrorMessage";
import type {
  Interaction,
  InteractionCreateInput,
  InteractionListItem,
  InteractionListParams,
  InteractionUpdateInput,
} from "@/types";

interface InteractionsState {
  items: InteractionListItem[];
  selected: Interaction | null;
  status: "idle" | "loading" | "succeeded" | "failed";
  error: string | null;
}

const initialState: InteractionsState = {
  items: [],
  selected: null,
  status: "idle",
  error: null,
};

export const fetchInteractions = createAsyncThunk<
  InteractionListItem[],
  InteractionListParams | undefined,
  { rejectValue: string }
>("interactions/fetchInteractions", async (params, { rejectWithValue }) => {
  try {
    return await interactionsApi.listInteractions(params);
  } catch (error) {
    return rejectWithValue(getErrorMessage(error));
  }
});

export const fetchInteraction = createAsyncThunk<Interaction, number, { rejectValue: string }>(
  "interactions/fetchInteraction",
  async (id, { rejectWithValue }) => {
    try {
      return await interactionsApi.getInteraction(id);
    } catch (error) {
      return rejectWithValue(getErrorMessage(error));
    }
  },
);

export const createInteraction = createAsyncThunk<
  Interaction,
  InteractionCreateInput,
  { rejectValue: string }
>("interactions/createInteraction", async (input, { rejectWithValue }) => {
  try {
    return await interactionsApi.createInteraction(input);
  } catch (error) {
    return rejectWithValue(getErrorMessage(error));
  }
});

export const updateInteraction = createAsyncThunk<
  Interaction,
  { id: number; data: InteractionUpdateInput },
  { rejectValue: string }
>("interactions/updateInteraction", async ({ id, data }, { rejectWithValue }) => {
  try {
    return await interactionsApi.updateInteraction(id, data);
  } catch (error) {
    return rejectWithValue(getErrorMessage(error));
  }
});

const interactionsSlice = createSlice({
  name: "interactions",
  initialState,
  reducers: {
    clearSelected(state) {
      state.selected = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchInteractions.pending, (state) => {
        state.status = "loading";
        state.error = null;
      })
      .addCase(fetchInteractions.fulfilled, (state, action) => {
        state.status = "succeeded";
        state.items = action.payload;
      })
      .addCase(fetchInteractions.rejected, (state, action) => {
        state.status = "failed";
        state.error = action.payload ?? "Could not load interactions.";
      });

    builder.addCase(fetchInteraction.fulfilled, (state, action) => {
      state.selected = action.payload;
    });

    builder.addCase(updateInteraction.fulfilled, (state, action) => {
      if (state.selected?.id === action.payload.id) {
        state.selected = action.payload;
      }
    });
  },
});

export const { clearSelected } = interactionsSlice.actions;
export default interactionsSlice.reducer;
