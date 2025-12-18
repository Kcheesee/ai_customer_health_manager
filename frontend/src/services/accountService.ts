import type { Account, AccountCreate } from "../types/account";

const API_URL = "http://localhost:8000/api/v1"; // TODO: Env var

export const accountService = {
    getAccounts: async (): Promise<Account[]> => {
        const response = await fetch(`${API_URL}/accounts/`);
        if (!response.ok) throw new Error("Failed to fetch accounts");
        return response.json();
    },

    getAccount: async (id: string): Promise<Account> => {
        const response = await fetch(`${API_URL}/accounts/${id}`);
        if (!response.ok) throw new Error("Failed to fetch account");
        return response.json();
    },

    createAccount: async (account: AccountCreate): Promise<Account> => {
        const response = await fetch(`${API_URL}/accounts/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(account),
        });
        if (!response.ok) throw new Error("Failed to create account");
        return response.json();
    },

    getChildren: async (id: string): Promise<Account[]> => {
        const response = await fetch(`${API_URL}/accounts/${id}/children`);
        if (!response.ok) throw new Error("Failed to fetch account children");
        return response.json();
    },
};
