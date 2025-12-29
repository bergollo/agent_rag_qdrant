// messagesSlice.ts

import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import type { RootState } from "../../app/store";
// import type { Message } from "../../types/messages";
import { uploadDocument } from "../../services/documentAPI";

interface StoreDocumentState {
  loading: boolean;
  error: string | null;
}

const initialState: StoreDocumentState = {
  loading: false,
  error: null,
};

// -----------------------------
// Async Thunks
// -----------------------------  
export const upload = createAsyncThunk<
  void,
  File,              
  { state: RootState }
>(
  "storeDocument/upload",
  async (document) => {
    // Example: replace with RTK Query or your real API
    const response = await uploadDocument(document);
    if (!response.ok) throw new Error("Failed to load messages");
    return;
  }
);

// -----------------------------
// Slice
// -----------------------------
const storeDocumentSlice = createSlice({
  name: "storeDocument",
  initialState,
  reducers: {},

  extraReducers: (builder) => {
    builder
      .addCase(upload.pending, (state) => {
        state.loading = true;
        state.error = null;
      })

      .addCase(upload.fulfilled, (state) => {
        state.loading = false;
      })

      .addCase(upload.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message ?? "Unknown error";
      });
  },
});

export default storeDocumentSlice.reducer;