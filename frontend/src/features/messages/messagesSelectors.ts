import type { RootState } from "../../app/store";
import { createSelector } from "@reduxjs/toolkit";

// Select the messages slice state
export const selectMessagesState = (state: RootState) => state.messages;

// Select all messages
export const selectAllMessages = createSelector(
  [selectMessagesState],
  (messagesState) => messagesState.items
);

// Select loading status
export const selectMessagesLoading = createSelector(
  [selectMessagesState],
  (messagesState) => messagesState.loading
);

// Select messages for a single conversation
export const selectMessagesForConversation = (conversationId: string) =>
  createSelector([selectAllMessages], (messages) =>
    messages.filter((m) => m.id === conversationId)
  );

// Select the last message in a conversation
export const selectLastMessage = (conversationId: string) =>
  createSelector([selectMessagesForConversation(conversationId)], (msgs) =>
    msgs[msgs.length - 1] ?? null
  );
