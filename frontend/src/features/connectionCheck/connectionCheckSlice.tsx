// connectionCheckSlice.ts

import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import type { RootState } from "../../app/store";
import { fetchBackendHC, fetchAiHC } from "../../services/healthz-check";

export type StatusType = 'unknown' | 'idle' | 'loading' | 'succeeded' | 'failed';

interface ConnectionState {
  backendStatus: StatusType;
  aiStatus: StatusType;
  backendLoading: boolean;
  aiLoading: boolean;
  backendError: string | null;
  aiError: string | null;
}

const initialState: ConnectionState = {
  backendStatus: "unknown",
  aiStatus: "unknown",
  backendLoading: false,
  aiLoading: false,
  backendError: null,
  aiError: null,
};

export const fetchConnection = createAsyncThunk<
  object,
  void,
  { state: RootState }
>(
  "api/connection",
  async () => {
    try {
      const res = await fetchBackendHC()
      if (!res.ok) throw new Error("Fail to check backend connection");
      return "succeeded";
    } catch (error: unknown) {
      console.error("Error in fetchConnection thunk:", error);
      throw error;
    }
  }
);

export const fetchAiConnection = createAsyncThunk<
  object,
  void,
  { state: RootState }
>(
  "api/ai/connection",
  async () => {
    const res = await fetchAiHC();
    if (!res.ok) throw new Error("Fail to check AI connection");
    return "succeeded" as StatusType;
  }
);

// -----------------------------
// Slice
// -----------------------------
const connectionCheckSlice = createSlice({
  name: "connectionCheck",
  initialState,
  reducers: {
    resetConnectionState: (state) => {
      state.backendStatus = "unknown";
      state.aiStatus = "unknown";
      state.backendLoading = false;
      state.aiLoading = false;
      state.backendError = null;
      state.aiError = null;
    }
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchConnection.pending, (state) => {
        state.backendLoading = true;
        state.backendError = null;
      })

      .addCase(fetchConnection.fulfilled, (state) => {
        state.backendLoading = false;
        // state.backendStatus = status;
        // console.log("Status:", state.backendStatus);
        state.backendStatus = "succeeded";
      })

      .addCase(fetchConnection.rejected, (state, action) => {
        state.backendLoading = false;
        state.backendStatus = "failed";
        state.backendError = action.error.message ?? "Fail";
      });

      builder
      .addCase(fetchAiConnection.pending, (state) => {
        state.aiLoading = true;
        state.aiError = null;
      })

      .addCase(fetchAiConnection.fulfilled, (state) => {
        state.aiLoading = false;
        // const status: string = action.payload;
        // state.aiStatus = status;
        state.aiStatus = "succeeded";
      })

      .addCase(fetchAiConnection.rejected, (state, action) => {
        state.aiLoading = false;
        state.aiStatus = "failed";
        state.aiError = action.error.message ?? "Fail";
      });
  },
});

export const { resetConnectionState } = connectionCheckSlice.actions;

export default connectionCheckSlice.reducer;