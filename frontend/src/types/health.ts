export interface HealthScore {
    id: string;
    account_id: string;
    overall_score: number;
    overall_status: "healthy" | "warning" | "at_risk";
    sentiment_score: number;
    engagement_score: number;
    request_score: number;
    relationship_score: number;
    satisfaction_score: number;
    expansion_score: number;
    ai_summary: string;
    calculated_at: string;
}
