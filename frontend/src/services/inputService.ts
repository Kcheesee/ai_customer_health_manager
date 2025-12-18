import type { InputCreate, InputResponse } from "../types/input";

const API_URL = "http://localhost:8000/api/v1";

export const inputService = {
    createInput: async (data: InputCreate): Promise<InputResponse> => {
        const response = await fetch(`${API_URL}/inputs/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });
        if (!response.ok) throw new Error("Failed to create input");
        return response.json();
    },

    getInputs: async (accountId: string): Promise<any[]> => {
        // Assuming backend has GET /inputs/account/{id} or filtered list
        // Creating this endpoint might be needed if not exists.
        // Checking routes...
        const response = await fetch(`${API_URL}/inputs/accounts/${accountId}`);
        if (!response.ok) throw new Error("Failed to fetch inputs");
        return response.json();
    },

    getAllInputs: async (): Promise<any[]> => {
        const response = await fetch(`${API_URL}/inputs/`);
        if (!response.ok) throw new Error("Failed to fetch all inputs");
        return response.json();
    },

    updateInput: async (id: string, data: any): Promise<any> => {
        const response = await fetch(`${API_URL}/inputs/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });
        if (!response.ok) throw new Error("Failed to update input");
        return response.json();
    }
};
