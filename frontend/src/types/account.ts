export const AccountType = {
    STANDARD: "standard",
    ELA_PARENT: "ela_parent",
    ELA_CHILD: "ela_child",
} as const;

export type AccountType = (typeof AccountType)[keyof typeof AccountType];

export const Tier = {
    ENTERPRISE: "enterprise",
    MID_MARKET: "mid_market",
    SMB: "smb",
    STARTUP: "startup",
} as const;

export type Tier = (typeof Tier)[keyof typeof Tier];

export interface Account {
    id: string;
    name: string;
    account_type: AccountType;
    account_email?: string;
    industry?: string;
    tier?: Tier;
    owner_id?: string;
    parent_account_id?: string;
    check_in_interval_days: number;
    is_active: boolean;
    children_count?: number;
    created_at?: string;
}

export interface AccountCreate {
    name: string;
    account_type: AccountType;
    account_email?: string;
    industry?: string;
    tier?: Tier;
    owner_id?: string;
    parent_account_id?: string;
    check_in_interval_days?: number;
}
