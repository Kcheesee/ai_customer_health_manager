import axios from "axios";
import type { Alert } from "@/types/alert";

const API_URL = "http://localhost:8000/api/v1";

export const alertService = {
    getAlerts: async (): Promise<Alert[]> => {
        const response = await axios.get(`${API_URL}/alerts/`);
        return response.data;
    },

    markAsRead: async (alertId: string): Promise<Alert> => {
        const response = await axios.put(`${API_URL}/alerts/${alertId}/read`);
        return response.data;
    },

    markAllRead: async (): Promise<void> => {
        await axios.put(`${API_URL}/alerts/read-all`);
    }
};
