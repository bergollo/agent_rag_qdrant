import { combineReducers } from "@reduxjs/toolkit";
import chat from "../features/messages/messagesSlice";

const rootReducer = combineReducers({
  chat,
});

export default rootReducer;
