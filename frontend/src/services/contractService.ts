import type { Contract, ContractCreate } from '../types/contract';

const API_BASE_URL = 'http://localhost:8000/api/v1';

export const contractService = {
    getContracts: async (accountId: string): Promise<Contract[]> => {
        const token = localStorage.getItem('token');
        const response = await fetch(`${API_BASE_URL}/contracts/accounts/${accountId}/contracts`, {
            headers: {
                'Authorization': `Bearer ${token}`,
            },
        });

        if (!response.ok) {
            throw new Error('Failed to fetch contracts');
        }

        return response.json();
    },

    createContract: async (contract: ContractCreate): Promise<Contract> => {
        const token = localStorage.getItem('token');
        const response = await fetch(`${API_BASE_URL}/contracts/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`,
            },
            body: JSON.stringify(contract),
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || 'Failed to create contract');
        }

        return response.json();
    },

    getAllContracts: async (): Promise<Contract[]> => {
        const token = localStorage.getItem('token');
        const response = await fetch(`${API_BASE_URL}/contracts/`, {
            headers: {
                'Authorization': `Bearer ${token}`,
            },
        });

        if (!response.ok) {
            throw new Error('Failed to fetch all contracts');
        }

        return response.json();
    },

    // Placeholder for update/delete if needed later
};
