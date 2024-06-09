import { createSlice, createAsyncThunk, PayloadAction } from "@reduxjs/toolkit";
import { userConfirmation, userRegistration, userLogout, userLogin } from "../utilities";
import { act } from "react";

interface AuthState {
    user: any;
    token: string | null;
    loading: boolean;
    error: string| null;
};

const initialState: AuthState = {
    user: null,
    token: localStorage.getItem('token'),
    loading: false,
    error: null,
};

export const confirmUser = createAsyncThunk('auth/confirmUser', async (_, thunkAPI) => {
    try {
        const user = await userConfirmation();
        return user;
    } catch (error) {
        return thunkAPI.rejectWithValue(error.response?.data || 'Error confirming user');
    }
});

export const registerUser = createAsyncThunk('auth/registerUser', async ({email, password}: {email: string, password: string}, thunkAPI) => {
    try {
        const user = await userRegistration(email, password);
        return user;
    } catch (error) {
        return thunkAPI.rejectWithValue(error.response?.data || 'Error registering user');
    }
});

export const loginUser = createAsyncThunk('auth/loginUser', async ({ email, password }: { email: string, password: string }, thunkAPI) => {
    try {
        const user = await userLogin(email, password);
        return user;
    } catch (error) {
        return thunkAPI.rejectWithValue(error.response?.data || 'Error logging in');
    }
});

export const logoutUser = createAsyncThunk('auth/logoutUser', async (_, thunkAPI) => {
    try {
        await userLogout();
        return true;
    } catch (error) {
        return thunkAPI.rejectWithValue(error.response?.data || 'Error logging out');
    }
});

const authSlice = createSlice({
  name: "auth",
  initialState,
  reducers: {
    resetError(state) {
        state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
        // user confirmation
        .addCase(confirmUser.pending, (state) => {
            state.loading = true;
            state.error = null;
        })
        .addCase(confirmUser.fulfilled, (state, action: PayloadAction<any>) => {
            state.loading = false;
            state.user = action.payload;
        })
        .addCase(confirmUser.rejected, (state, action: PayloadAction<any>) => {
            state.loading = false;
            state.error = action.payload;
        })
        // user registration
        .addCase(registerUser.pending, (state) => {
            state.loading = true;
            state.error = null;
        })
        .addCase(registerUser.fulfilled, (state, action: PayloadAction<any>) => {
            state.loading = false;
            state.user = action.payload;
        })
        .addCase(registerUser.rejected, (state, action: PayloadAction<any>) => {
            state.loading = false;
            state.error = action.payload;
        })
        // user login
      .addCase(loginUser.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(loginUser.fulfilled, (state, action: PayloadAction<any>) => {
        state.loading = false;
        state.user = action.payload;
        state.token = localStorage.getItem("token");
      })
      .addCase(loginUser.rejected, (state, action: PayloadAction<any>) => {
        state.loading = false;
        state.error = action.payload;
      })
      // user logout
      .addCase(logoutUser.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(logoutUser.fulfilled, (state) => {
        state.loading = false;
        state.user = null;
        state.token = null;
      })
      .addCase(logoutUser.rejected, (state, action: PayloadAction<any>) => {
        state.loading = false;
        state.error = action.payload;
      });
  }
});

export const { resetError } = authSlice.actions;

export default authSlice.reducer;