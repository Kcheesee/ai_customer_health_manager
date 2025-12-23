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
    ato_status: string; // none, pending, active, expired
    ato_expiry_date?: string | null;

    // Content
    full_text?: string;
    document_path?: string;
}

export interface ContractCreate extends Omit<Contract, 'id' | 'created_at' | 'updated_at'> {
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
