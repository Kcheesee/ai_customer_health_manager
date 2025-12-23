export interface AccountDocument {
    id: string;
    account_id: string;
    name: string;
    file_path: string;
    file_type?: string;
    created_at: string;
}
