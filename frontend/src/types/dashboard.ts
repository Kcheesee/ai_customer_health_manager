export interface DashboardStats {
    total_accounts: number;
    health_distribution: {
        healthy: number;
        warning: number;
        at_risk: number;
    };
    average_score: number;
    upcoming_renewals?: UpcomingRenewal[];
    arr_at_risk?: number;
}

export interface UpcomingRenewal {
    id: string;
    account_name: string;
    contract_name: string;
    end_date: string;
    arr: number;
}

export interface RiskyAccount {
    id: string;
    name: string;
    tier: string;
    score: number;
    status: "healthy" | "warning" | "at_risk";
    industry?: string;
    last_updated: string;
}
