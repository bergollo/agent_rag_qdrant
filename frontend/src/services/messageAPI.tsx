// src/services/health-check.tsx

import { config } from "../config";
import type { Message } from "../types/messages";

// AI Server LLM Query
export const agentLLMQuery = async (message: Message): Promise<Response> => {
    try {
        const response = await fetch(`${config.API_BASE_URL}/api/ai/query`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: message.text }),
        });
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response;
    } catch (error) {
        console.error('Error fetching user data:', error);
        throw error;
    }
};