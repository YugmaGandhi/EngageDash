import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";

import * as customersApi from "@/lib/api/customers";
import { getErrorMessage } from "@/lib/getErrorMessage";
import type {
  Customer,
  CustomerCreateInput,
  CustomerListItem,
  CustomerListParams,
  CustomerUpdateInput,
} from "@/types";

interface CustomersState {
  items: CustomerListItem[]; // the list
  selected: Customer | null; // the customer being viewed/edited
  status: "idle" | "loading" | "succeeded" | "failed";
  error: string | null;
}

const initialState: CustomersState = {
  items: [],
  selected: null,
  status: "idle",
  error: null,
};

export const fetchCustomers = createAsyncThunk<
  CustomerListItem[],
  CustomerListParams | undefined,
  { rejectValue: string }
>("customers/fetchCustomers", async (params, { rejectWithValue }) => {
  try {
    return await customersApi.listCustomers(params);
  } catch (error) {
    return rejectWithValue(getErrorMessage(error));
  }
});

export const fetchCustomer = createAsyncThunk<Customer, number, { rejectValue: string }>(
  "customers/fetchCustomer",
  async (id, { rejectWithValue }) => {
    try {
      return await customersApi.getCustomer(id);
    } catch (error) {
      return rejectWithValue(getErrorMessage(error));
    }
  },
);

export const createCustomer = createAsyncThunk<
  Customer,
  CustomerCreateInput,
  { rejectValue: string }
>("customers/createCustomer", async (input, { rejectWithValue }) => {
  try {
    return await customersApi.createCustomer(input);
  } catch (error) {
    return rejectWithValue(getErrorMessage(error));
  }
});

export const updateCustomer = createAsyncThunk<
  Customer,
  { id: number; data: CustomerUpdateInput },
  { rejectValue: string }
>("customers/updateCustomer", async ({ id, data }, { rejectWithValue }) => {
  try {
    return await customersApi.updateCustomer(id, data);
  } catch (error) {
    return rejectWithValue(getErrorMessage(error));
  }
});

export const deleteCustomer = createAsyncThunk<number, number, { rejectValue: string }>(
  "customers/deleteCustomer",
  async (id, { rejectWithValue }) => {
    try {
      await customersApi.deleteCustomer(id);
      return id; // return the id so we can remove it from the list
    } catch (error) {
      return rejectWithValue(getErrorMessage(error));
    }
  },
);

const customersSlice = createSlice({
  name: "customers",
  initialState,
  reducers: {
    clearSelected(state) {
      state.selected = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchCustomers.pending, (state) => {
        state.status = "loading";
        state.error = null;
      })
      .addCase(fetchCustomers.fulfilled, (state, action) => {
        state.status = "succeeded";
        state.items = action.payload;
      })
      .addCase(fetchCustomers.rejected, (state, action) => {
        state.status = "failed";
        state.error = action.payload ?? "Could not load customers.";
      });

    builder.addCase(fetchCustomer.fulfilled, (state, action) => {
      state.selected = action.payload;
    });

    // Keep the detail view in sync after an edit.
    builder.addCase(updateCustomer.fulfilled, (state, action) => {
      if (state.selected?.id === action.payload.id) {
        state.selected = action.payload;
      }
    });

    // Remove the deleted customer from the list immediately.
    builder.addCase(deleteCustomer.fulfilled, (state, action) => {
      state.items = state.items.filter((c) => c.id !== action.payload);
    });
  },
});

export const { clearSelected } = customersSlice.actions;
export default customersSlice.reducer;
