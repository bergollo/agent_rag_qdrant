// messagesSlice.ts

import { createSlice, createAsyncThunk, type PayloadAction } from "@reduxjs/toolkit";
import type { RootState } from "../../app/store";
import type { Message } from "../../types/messages";
import { loadFromStorage, saveToStorage } from "../../utils/persist";
import { agentLLMQuery } from "../../services/messageAPI";

// -----------------------------
// Types
// -----------------------------
interface MessagesState {
  items: Message[];
  loading: boolean;
  error: string | null;
}

const STORAGE_KEY = "messages";

// Load persisted messages (optional)
const initialState: MessagesState = {
  items: loadFromStorage<Message[]>(STORAGE_KEY, []),
  loading: false,
  error: null,
};

// -----------------------------
// Async Thunks (example)
// -----------------------------
export const fetchMessages = createAsyncThunk<
  Message[],           // return value
  string,              // conversationId
  { state: RootState } // thunkAPI
>(
  "messages/fetchMessages",
  async (conversationId) => {
    // Example: replace with RTK Query or your real API
    const response = await fetch(`/api/messages/${conversationId}`);
    if (!response.ok) throw new Error("Failed to load messages");

    return (await response.json()) as Message[];
  }
);

// -----------------------------
// New Thunk: AI Query
// -----------------------------
export const messageQuery = createAsyncThunk<
  Message,             // return type (AI message)
  { userMessage: Message },// argument type
  { state: RootState }
>(
  "messages/ai/query",
  async ({ userMessage }) => {
    console.log("AI query with user message:", userMessage);
    const res = await agentLLMQuery(userMessage);

    if (!res.ok) throw new Error("AI request failed");

    const data = await res.json();

    // Ensure returned Message shape
    const aiMessage: Message = {
      id: data.id,
      sender: "bot",
      text: data.answer || data.result || "No response",
      createdAt: new Date().toISOString(),
      status: "sent"
    };

    return aiMessage;
  }
);

// -----------------------------
// Slice
// -----------------------------
const messagesSlice = createSlice({
  name: "messages",
  initialState,
  reducers: {
    // Add a new incoming message (supports WebSocket events)
    addMessage(state, action: PayloadAction<Message>) {
      state.items.push(action.payload);
      saveToStorage(STORAGE_KEY, state.items);
    },

    // Update (edit) existing message
    updateMessage(state, action: PayloadAction<Message>) {
      const index = state.items.findIndex(
        (m) => m.id === action.payload.id
      );
      if (index !== -1) {
        state.items[index] = action.payload;
        saveToStorage(STORAGE_KEY, state.items);
      }
    },

    // Remove message by id
    deleteMessage(state, action: PayloadAction<string>) {
      state.items = state.items.filter((m) => m.id !== action.payload);
      saveToStorage(STORAGE_KEY, state.items);
    },
  },

  // -----------------------------
  // Async thunk reducers
  // -----------------------------
  extraReducers: (builder) => {
    builder
      .addCase(fetchMessages.pending, (state) => {
        state.loading = true;
        state.error = null;
      })

      .addCase(fetchMessages.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload;
        saveToStorage(STORAGE_KEY, state.items);
      })

      .addCase(fetchMessages.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message ?? "Unknown error";
      });

      builder
        .addCase(messageQuery.pending, (state) => {
          state.loading = true;
          state.error = null;
        })
        .addCase(messageQuery.fulfilled, (state, action) => {
          state.loading = false;
          state.items.push(action.payload);
          saveToStorage(STORAGE_KEY, state.items);
        })
        .addCase(messageQuery.rejected, (state, action) => {
          state.loading = false;
          state.error = action.error.message ?? "Unknown error";
        });
  },
});

export const { addMessage, updateMessage, deleteMessage } = messagesSlice.actions;

export default messagesSlice.reducer;