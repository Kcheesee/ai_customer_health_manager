export interface InputCreate {
    account_id: string;
    content: string;
    input_type: "email" | "call" | "ticket" | "meeting_note";
    sender?: string;
    content_date?: string;
}

export interface InputResponse {
    status: string;
    extraction: any;
}

export interface Input {
    id: string;
    content: string;
    input_type: string;
    sender: string;
    content_date: string;
    created_at?: string;
    is_processed: boolean;
}
