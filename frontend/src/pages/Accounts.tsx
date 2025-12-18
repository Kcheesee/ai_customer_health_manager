import { useEffect, useState } from "react";
import type { Account } from "@/types/account";
import { accountService } from "@/services/accountService";
import { AccountList } from "@/components/accounts/AccountList";
import { AddAccountModal } from "@/components/accounts/AddAccountModal";

export default function AccountsPage() {
    const [accounts, setAccounts] = useState<Account[]>([]);
    const [loading, setLoading] = useState(true);

    const fetchAccounts = async () => {
        try {
            const data = await accountService.getAccounts();
            setAccounts(data);
        } catch (error) {
            console.error(error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchAccounts();
    }, []);

    return (
        <div className="flex-1 space-y-4 p-8 pt-6">
            <div className="flex items-center justify-between space-y-2">
                <h2 className="text-3xl font-bold tracking-tight">Accounts</h2>
                <div className="flex items-center space-x-2">
                    <AddAccountModal onAccountAdded={fetchAccounts} />
                </div>
            </div>
            {loading ? (
                <div>Loading...</div>
            ) : (
                <AccountList accounts={accounts} />
            )}
        </div>
    );
}
