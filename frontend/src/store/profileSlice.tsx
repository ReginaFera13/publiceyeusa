import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { getUserProfile, putUserProfile } from "../utilities";

interface ProfileState {
  profile: any; 
  loading: boolean;
  error: string | null;
}

const initialState: ProfileState = {
  profile: null,
  loading: false,
  error: null,
};

export const fetchProfile = createAsyncThunk("profile/fetchProfile", async () => {
  try {
    const data = await getUserProfile(); // Adjust this based on your API function to fetch profile
    return data;
  } catch (error) {
    throw error;
  }
});

export const updateProfile = createAsyncThunk(
  "profile/updateProfile",
  async (profileData: any) => {
    try {
      const updatedData = await putUserProfile(profileData); // Adjust this based on your API function to update profile
      return updatedData;
    } catch (error) {
      throw error;
    }
  }
);

const profileSlice = createSlice({
  name: "profile",
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchProfile.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchProfile.fulfilled, (state, action) => {
        state.loading = false;
        state.profile = action.payload;
      })
      .addCase(fetchProfile.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || "Failed to fetch profile";
      })
      .addCase(updateProfile.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(updateProfile.fulfilled, (state, action) => {
        state.loading = false;
        state.profile = action.payload;
      })
      .addCase(updateProfile.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || "Failed to update profile";
      });
  },
});

export default profileSlice.reducer;