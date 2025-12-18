import type { DashboardStats, RiskyAccount } from "../types/dashboard";

const API_URL = "http://localhost:8000/api/v1";

export const dashboardService = {
    getStats: async (): Promise<DashboardStats> => {
        const response = await fetch(`${API_URL}/dashboard/stats`);
        if (!response.ok) throw new Error("Failed to fetch dashboard stats");
        return response.json();
    },

    getRiskyAccounts: async (): Promise<RiskyAccount[]> => {
        const response = await fetch(`${API_URL}/dashboard/risky`);
        if (!response.ok) throw new Error("Failed to fetch risky accounts");
        return response.json();
    },
};
