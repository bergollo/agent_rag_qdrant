import { config } from "../config";
import { configureStore } from "@reduxjs/toolkit";
import connectionReducer from "../features/connectionCheck/connectionCheckSlice";
import messagesReducer from "../features/messages/messagesSlice";
import storeDocument from "../features/storeDocument/storeDocumentSlice";
// import authReducer from "../features/auth/authSlice";
// import conversationsReducer from "@/features/conversations/conversationsSlice";

// --------------------------------------------
// Store Configuration
// --------------------------------------------
export const store = configureStore({
  reducer: {
    connection: connectionReducer,
    messages: messagesReducer,
    storeDocument: storeDocument,
    // auth: authReducer,
    // conversations: conversationsReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: false, // common for WebSocket/persist situations
    }),
  devTools: config.NODE_ENV !== "production",
});

// --------------------------------------------
// Types
// --------------------------------------------
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

