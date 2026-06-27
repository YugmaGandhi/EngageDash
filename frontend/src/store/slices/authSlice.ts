import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";

import * as authApi from "@/lib/api/auth";
import { getErrorMessage } from "@/lib/getErrorMessage";
import { clearTokens, setTokens } from "@/lib/tokenStorage";
import type { AppDispatch } from "@/store/store";
import type { LoginInput, RegisterInput, User } from "@/types";

interface AuthState {
  user: User | null;
  // idle = not checked yet, loading = a request is in flight.
  status: "idle" | "loading" | "authenticated" | "unauthenticated";
  error: string | null;
}

const initialState: AuthState = {
  user: null,
  status: "idle",
  error: null,
};

// Log in: get tokens, save them, then load the user's profile.
export const login = createAsyncThunk<User, LoginInput, { rejectValue: string }>(
  "auth/login",
  async (credentials, { rejectWithValue }) => {
    try {
      const tokens = await authApi.login(credentials);
      setTokens(tokens.access_token, tokens.refresh_token);
      return await authApi.getMe();
    } catch (error) {
      return rejectWithValue(getErrorMessage(error, "Invalid email or password."));
    }
  },
);

// Register, then log in with the same credentials so the user is signed in.
export const register = createAsyncThunk<User, RegisterInput, { rejectValue: string }>(
  "auth/register",
  async (input, { rejectWithValue }) => {
    try {
      await authApi.register(input);
      const tokens = await authApi.login({ email: input.email, password: input.password });
      setTokens(tokens.access_token, tokens.refresh_token);
      return await authApi.getMe();
    } catch (error) {
      return rejectWithValue(getErrorMessage(error, "Registration failed."));
    }
  },
);

// Load the current user from the saved token (used to restore the session on reload).
export const fetchProfile = createAsyncThunk("auth/fetchProfile", async () => {
  return authApi.getMe();
});

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    clearAuth(state) {
      state.user = null;
      state.status = "unauthenticated";
      state.error = null;
    },
    setUser(state, action: { payload: User }) {
      state.user = action.payload;
      state.status = "authenticated";
    },
    clearError(state) {
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    // login, register, and fetchProfile all end with an authenticated user.
    for (const thunk of [login, register, fetchProfile]) {
      builder.addCase(thunk.pending, (state) => {
        state.status = "loading";
        state.error = null;
      });
      builder.addCase(thunk.fulfilled, (state, action) => {
        state.user = action.payload;
        state.status = "authenticated";
      });
    }
    builder.addCase(login.rejected, (state, action) => {
      state.status = "unauthenticated";
      state.error = action.payload ?? "Login failed.";
    });
    builder.addCase(register.rejected, (state, action) => {
      state.status = "unauthenticated";
      state.error = action.payload ?? "Registration failed.";
    });
    builder.addCase(fetchProfile.rejected, (state) => {
      state.status = "unauthenticated";
      state.user = null;
    });
  },
});

export const { clearAuth, setUser, clearError } = authSlice.actions;

// Log out: clear the saved tokens and reset auth state.
export const logout = () => (dispatch: AppDispatch) => {
  clearTokens();
  dispatch(clearAuth());
};

export default authSlice.reducer;
