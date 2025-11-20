// src/services/health-check.tsx

import { config } from "../config";
// import type { Message } from "../types/messages";

// AI Server LLM Query
export const uploadDocument = async (document:File): Promise<Response> => {
    try {
        const datafile = new FormData();
        datafile.append('file', document);
        console.log(document)
        const response = await fetch(`${config.API_BASE_URL}/api/ai/vectorstore/upload`, {
            method: 'POST',
            body: datafile,
        });
        if (!response.ok) {
            throw new Error('Error uploading document');
        }
        return response;
    } catch (error) {
        console.error('Error fetching user data:', error);
        throw error;
    }
};