import axios from "axios";

export interface Reminder {
    id: string;
    account_id: string;
    source_input_id?: string;
    description: string;
    due_date?: string;
    is_completed: boolean;
    created_at: string;
}

const API_URL = "http://localhost:8000/api/v1";

export const reminderService = {
    getReminders: async (accountId: string): Promise<Reminder[]> => {
        const response = await axios.get(`${API_URL}/reminders/`, { params: { account_id: accountId } });
        return response.data;
    },

    createReminder: async (accountId: string, description: string, dueDate?: Date): Promise<Reminder> => {
        const response = await axios.post(`${API_URL}/reminders/`, {
            account_id: accountId,
            description,
            due_date: dueDate?.toISOString()
        });
        return response.data;
    },

    updateReminder: async (id: string, updates: Partial<Reminder>): Promise<Reminder> => {
        const response = await axios.put(`${API_URL}/reminders/${id}`, updates);
        return response.data;
    },

    deleteReminder: async (id: string): Promise<void> => {
        await axios.delete(`${API_URL}/reminders/${id}`);
    }
};
