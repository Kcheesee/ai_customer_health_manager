import type { AccountDocument } from "@/types/document";

const API_BASE_URL = 'http://localhost:8000/api/v1';

export const documentService = {
    getDocuments: async (accountId: string): Promise<AccountDocument[]> => {
        const token = localStorage.getItem('token');
        const response = await fetch(`${API_BASE_URL}/documents/account/${accountId}`, {
            headers: {
                'Authorization': `Bearer ${token}`,
            },
        });

        if (!response.ok) {
            throw new Error('Failed to fetch documents');
        }

        return response.json();
    },

    uploadDocument: async (accountId: string, file: File): Promise<AccountDocument> => {
        const token = localStorage.getItem('token');
        const formData = new FormData();
        formData.append('file', file);

        // Add account_id as query param or generic parsing dependent on backend
        // My backend expects account_id query param for simplicity or body field
        // Let's use query param for this specific route setup based on my backend code:
        // @router.post("/upload", ...) -> def upload_document(account_id: UUID, ...)

        const response = await fetch(`${API_BASE_URL}/documents/upload?account_id=${accountId}`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
            },
            body: formData,
        });

        if (!response.ok) {
            const error = await response.json().catch(() => ({}));
            throw new Error(error.detail || 'Failed to upload document');
        }

        return response.json();
    },

    deleteDocument: async (documentId: string): Promise<void> => {
        const token = localStorage.getItem('token');
        const response = await fetch(`${API_BASE_URL}/documents/${documentId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`,
            },
        });

        if (!response.ok) {
            throw new Error('Failed to delete document');
        }
    }
};
