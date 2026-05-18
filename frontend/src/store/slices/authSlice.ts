import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";

import { authService } from "../../services/authService";
import { getBackendErrorMessage } from "../../utils/extractErrorData";

interface User {
  id: number;
  username: string;
}

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  initialized: boolean;
  error: string | null;
}

const initialState: AuthState = {
  user: null,
  isAuthenticated: false,
  isLoading: false,
  initialized: false,
  error: null,
};

export const login = createAsyncThunk(
  "auth/login",

  async (
    credentials: {
      identifier: string;
      password: string;
    },
    thunkAPI,
  ) => {
    try {
      return await authService.login(
        credentials.identifier,
        credentials.password,
      );
    } catch (error: unknown) {
      return thunkAPI.rejectWithValue(
        getBackendErrorMessage(error) ?? "Login failed",
      );
    }
  },
);

export const loadUser = createAsyncThunk(
  "auth/loadUser",

  async (_, thunkAPI) => {
    try {
      return await authService.getCurrentUser();
    } catch {
      authService.logout();
      return thunkAPI.rejectWithValue("Failed to load user");
    }
  },
);

const authSlice = createSlice({
  name: "auth",

  initialState,

  reducers: {
    logout(state) {
      authService.logout();

      state.user = null;
      state.isAuthenticated = false;
      state.isLoading = false;
      state.error = null;
      state.initialized = true;
    },
  },

  extraReducers: (builder) => {
    builder
      .addCase(login.pending, (state) => {
        state.isLoading = true;
        state.error = null;
      })

      .addCase(login.fulfilled, (state, action) => {
        state.isLoading = false;
        state.isAuthenticated = true;
        state.user = action.payload.user;
        state.initialized = true;
      })

      .addCase(login.rejected, (state, action) => {
        state.isLoading = false;
        state.isAuthenticated = false;
        state.user = null;
        state.error = action.payload as string;
        state.initialized = true;
      })
      .addCase(loadUser.pending, (state) => {
        state.isLoading = true;
      })
      .addCase(loadUser.fulfilled, (state, action) => {
        state.user = action.payload;
        state.isAuthenticated = true;
        state.isLoading = false;
        state.initialized = true;
      })

      .addCase(loadUser.rejected, (state) => {
        state.user = null;
        state.isAuthenticated = false;
        state.isLoading = false;
        state.initialized = true;
      });
  },
});

export const { logout } = authSlice.actions;

export default authSlice.reducer;
