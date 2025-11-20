import { createSlice, type PayloadAction } from "@reduxjs/toolkit";

type Toast = { id: string; message: string; type?: "info" | "success" | "error"; ttl?: number };

type UIState = {
  locale: string;
  isSidebarOpen: boolean;
  focusedInputId?: string | null;
  draftByConversation: Record<string, string>; // optional per-conversation drafts
  toasts: Toast[];
  isOffline: boolean;
  isSendingIndicatorOn: boolean;
};

const initialState: UIState = {
  locale: "en",
  isSidebarOpen: true,
  focusedInputId: null,
  draftByConversation: {},
  toasts: [],
  isOffline: false,
  isSendingIndicatorOn: false,
};

const uiSlice = createSlice({
  name: "ui",
  initialState,
  reducers: {
    setLocale(state, action: PayloadAction<string>) {
      state.locale = action.payload;
    },
    openSidebar(state) {
      state.isSidebarOpen = true;
    },
    closeSidebar(state) {
      state.isSidebarOpen = false;
    },
    setFocusedInput(state, action: PayloadAction<string | null>) {
      state.focusedInputId = action.payload;
    },
    setDraft(state, action: PayloadAction<{ conversationId: string; draft: string }>) {
      state.draftByConversation[action.payload.conversationId] = action.payload.draft;
    },
    clearDraft(state, action: PayloadAction<{ conversationId: string }>) {
      delete state.draftByConversation[action.payload.conversationId];
    },
    pushToast(state, action: PayloadAction<Toast>) {
      state.toasts.push(action.payload);
    },
    removeToast(state, action: PayloadAction<{ id: string }>) {
      state.toasts = state.toasts.filter((t) => t.id !== action.payload.id);
    },
    setOffline(state, action: PayloadAction<boolean>) {
      state.isOffline = action.payload;
    },
    setSendingIndicator(state, action: PayloadAction<boolean>) {
      state.isSendingIndicatorOn = action.payload;
    },
    clearToasts(state) {
      state.toasts = [];
    },
  },
});

export const {
  setLocale,
  openSidebar,
  closeSidebar,
  setFocusedInput,
  setDraft,
  clearDraft,
  pushToast,
  removeToast,
  setOffline,
  setSendingIndicator,
  clearToasts,
} = uiSlice.actions;

export default uiSlice.reducer;
