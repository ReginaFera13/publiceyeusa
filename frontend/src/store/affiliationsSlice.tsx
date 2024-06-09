import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { getAffilations } from "../utilities";

interface AffiliationsState {
  affiliations: any; 
  loading: boolean;
  error: string | null;
};

const initialState: AffiliationsState = {
  affiliations: null,
  loading: false,
  error: null,
};

export const fetchAffiliations = createAsyncThunk("affiliations/fetchAffiliations", async () => {
  try {
    const data = await getAffilations(); // Adjust this based on your API function to fetch profile
    return data;
  } catch (error) {
    throw error;
  }
});

const affiliationsSlice = createSlice({
  name: "affiliations",
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchAffiliations.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchAffiliations.fulfilled, (state, action) => {
        state.loading = false;
        state.affiliations = action.payload;
      })
      .addCase(fetchAffiliations.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || "Failed to fetch profile";
      })
  },
});

export default affiliationsSlice.reducer;