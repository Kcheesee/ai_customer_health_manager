import { useState, useEffect } from "react";
import { ContractList } from "@/components/contracts/ContractList";
import { contractService } from "@/services/contractService";
import type { Contract } from "@/types/contract";
import { Loader2 } from "lucide-react";

export default function ContractsPage() {
    const [contracts, setContracts] = useState<Contract[]>([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchContracts = async () => {
            try {
                const data = await contractService.getAllContracts();
                setContracts(data);
            } catch (err: any) {
                setError(err.message || "Failed to load contracts");
            } finally {
                setLoading(false);
            }
        };
        fetchContracts();
    }, []);

    return (
        <div className="space-y-6">
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold tracking-tight">Contract Management</h1>
                    <p className="text-muted-foreground">
                        Overview of all active contracts and renewals across the portfolio.
                    </p>
                </div>
            </div>

            {loading ? (
                <div className="flex h-[400px] items-center justify-center">
                    <Loader2 className="h-8 w-8 animate-spin text-primary" />
                </div>
            ) : error ? (
                <div className="p-4 bg-red-50 border border-red-200 text-red-700 rounded-md">
                    {error}
                </div>
            ) : (
                <div className="grid gap-6">
                    <ContractList
                        contracts={contracts}
                        onAddContract={() => {
                            // Optionally refresh global list
                        }}
                    />
                </div>
            )}
        </div>
    );
}
