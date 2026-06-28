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
  status: "idle" | "loading" | "succeeded" | "failed"; // the list
  error: string | null; // the list
  selectedStatus: "idle" | "loading" | "succeeded" | "failed"; // the single item
  selectedError: string | null; // the single item (e.g. not found)
}

const initialState: InteractionsState = {
  items: [],
  selected: null,
  status: "idle",
  error: null,
  selectedStatus: "idle",
  selectedError: null,
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
      state.selectedStatus = "idle";
      state.selectedError = null;
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

    builder
      .addCase(fetchInteraction.pending, (state) => {
        state.selectedStatus = "loading";
        state.selectedError = null;
      })
      .addCase(fetchInteraction.fulfilled, (state, action) => {
        state.selectedStatus = "succeeded";
        state.selected = action.payload;
      })
      .addCase(fetchInteraction.rejected, (state, action) => {
        state.selectedStatus = "failed";
        state.selectedError = action.payload ?? "Could not load interaction.";
        state.selected = null;
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
