import type { RootState } from "../../app/store";
import { createSelector } from "@reduxjs/toolkit";

export const selectStoreDocState = (state: RootState) => state.storeDocument;

// Select loading status
export const selectStoreDocumentLoading = createSelector(
  [selectStoreDocState],
  (storeDocument) => storeDocument.loading
);
