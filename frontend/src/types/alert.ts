export interface Alert {
    id: string;
    type: "info" | "warning" | "error" | "success";
    title: string;
    message: string;
    link?: string;
    is_read: boolean;
    created_at: string;
}
