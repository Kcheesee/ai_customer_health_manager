import type { HealthScore } from "../types/health";

const API_URL = "http://localhost:8000/api/v1";

export const healthService = {
    calculateScore: async (accountId: string): Promise<HealthScore> => {
        const response = await fetch(`${API_URL}/health/accounts/${accountId}/calculate`, {
            method: "POST",
        });
        if (!response.ok) throw new Error("Failed to calculate health score");
        return response.json();
    },

    getLatestHealth: async (accountId: string): Promise<HealthScore> => {
        const response = await fetch(`${API_URL}/health/accounts/${accountId}/history?limit=1`);
        if (!response.ok) throw new Error("Failed to fetch latest health score");
        const history = await response.json();
        return history[0];
    },

    getHistory: async (accountId: string): Promise<HealthScore[]> => {
        const response = await fetch(`${API_URL}/health/accounts/${accountId}/history`);
        if (!response.ok) throw new Error("Failed to fetch health history");
        return response.json();
    },
};
