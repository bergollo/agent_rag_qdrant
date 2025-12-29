// src/services/health-check.tsx

import { config } from "../config";

export const fetchAiHC = async (): Promise<Response> => {
    const controller = new AbortController();
    const id = setTimeout(() => controller.abort(), 3000);

    try {
        const response = await fetch(`${config.API_BASE_URL}/api/ai/healthz`,
        { signal: controller.signal });
        clearTimeout(id);
        if (!response.ok) {
        throw new Error('Network response was not ok');
        }
        return response;
    } catch (error) {
        clearTimeout(id);
        console.error('Error fetching user data:', error);
        throw error;
    }
};

export const fetchBackendHC = async (): Promise<Response> => {
    const controller = new AbortController();
    const id = setTimeout(() => controller.abort(), 3000);

    try {
        console.log(config)
        const response = await fetch(`${config.API_BASE_URL}/api/healthz`,
            { signal: controller.signal });
        clearTimeout(id);
        if (!response.ok) {
        throw new Error('Network response was not ok');
        }
        return response;
    } catch (error) {
        clearTimeout(id);
        console.error('Error fetching user data:', error);
        throw error;
    }
};