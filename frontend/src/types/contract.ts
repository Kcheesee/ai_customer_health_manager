export interface Contract {
    id: string;
    account_id: string;
    contract_name: string;
    contract_type: string;
    status: string;
    effective_date: string;
    end_date: string;
    term_length?: string;
    auto_renewal: boolean;
    notice_period_days: number;
    total_contract_value?: number;
    arr?: number;
    primary_signer?: string;
    products_modules: string[];
    created_at: string;
}

export interface ContractCreate {
    account_id: string;
    contract_name: string;
    contract_type: string;
    status: string;
    effective_date: string;
    end_date: string;
    term_length?: string;
    auto_renewal?: boolean;
    notice_period_days?: number;
    total_contract_value?: number;
    arr?: number;
    primary_signer?: string;
    products_modules?: string[];
}
