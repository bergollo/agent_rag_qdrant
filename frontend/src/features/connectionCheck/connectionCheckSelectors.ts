import type { RootState } from "../../app/store";
import { createSelector } from "@reduxjs/toolkit";

// Select connection slice state
export const selectConnectionState = (state: RootState) => state.connection;

// Select backend connection status
export const selectConnectionStatus = createSelector(
  [selectConnectionState],
  (connectionState) => connectionState.backendStatus
);

// Select AI connection status
export const selectAiConnectionStatus = createSelector(
  [selectConnectionState],
  (connectionState) => connectionState.aiStatus
);

// Select loading status
export const selectBackendConnLoading = createSelector(
  [selectConnectionState],
  (connectionState) => connectionState.backendLoading
);

// Select loading status
export const selectAiConnLoading = createSelector(
  [selectConnectionState],
  (connectionState) => connectionState.aiLoading
);
