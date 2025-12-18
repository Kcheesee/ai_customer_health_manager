import { useState } from "react";
import { Button } from "@/components/ui/button";
import {
    Dialog,
    DialogContent,
    DialogHeader,
    DialogTitle,
    DialogFooter,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import type { ContractCreate } from "@/types/contract";
import { contractService } from "@/services/contractService";

interface ContractModalProps {
    accountId: string;
    isOpen: boolean;
    onClose: () => void;
    onSuccess: () => void;
}

export function ContractModal({ accountId, isOpen, onClose, onSuccess }: ContractModalProps) {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    const [formData, setFormData] = useState<Partial<ContractCreate>>({
        contract_name: "",
        contract_type: "saas_subscription",
        status: "active",
        effective_date: "",
        end_date: "",
        arr: 0,
        term_length: "annual",
        auto_renewal: true
    });

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError("");

        try {
            await contractService.createContract({
                ...formData,
                account_id: accountId,
                arr: Number(formData.arr),
                // Ensure dates are string YYYY-MM-DD
            } as ContractCreate);

            onSuccess();
            onClose();
        } catch (err: any) {
            setError(err.message || "Failed to create contract");
        } finally {
            setLoading(false);
        }
    };

    return (
        <Dialog open={isOpen} onOpenChange={onClose}>
            <DialogContent className="sm:max-w-[500px]">
                <DialogHeader>
                    <DialogTitle>Add Contract</DialogTitle>
                </DialogHeader>

                <form onSubmit={handleSubmit} className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                        <div className="space-y-2">
                            <Label htmlFor="name">Contract Name</Label>
                            <Input
                                id="name"
                                required
                                value={formData.contract_name}
                                onChange={(e) => setFormData({ ...formData, contract_name: e.target.value })}
                                placeholder="MSA 2024"
                            />
                        </div>

                        <div className="space-y-2">
                            <Label htmlFor="type">Type</Label>
                            <Select
                                value={formData.contract_type}
                                onValueChange={(val) => setFormData({ ...formData, contract_type: val })}
                            >
                                <SelectTrigger>
                                    <SelectValue placeholder="Select type" />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="saas_subscription">SaaS Subscription</SelectItem>
                                    <SelectItem value="consulting_sow">Consulting SOW</SelectItem>
                                    <SelectItem value="msa">MSA</SelectItem>
                                </SelectContent>
                            </Select>
                        </div>
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                        <div className="space-y-2">
                            <Label htmlFor="arr">ARR ($)</Label>
                            <Input
                                id="arr"
                                type="number"
                                value={formData.arr}
                                onChange={(e) => setFormData({ ...formData, arr: Number(e.target.value) })}
                            />
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="status">Status</Label>
                            <Select
                                value={formData.status}
                                onValueChange={(val) => setFormData({ ...formData, status: val })}
                            >
                                <SelectTrigger>
                                    <SelectValue />
                                </SelectTrigger>
                                <SelectContent>
                                    <SelectItem value="active">Active</SelectItem>
                                    <SelectItem value="draft">Draft</SelectItem>
                                    <SelectItem value="pending_renewal">Pending Renewal</SelectItem>
                                </SelectContent>
                            </Select>
                        </div>
                    </div>

                    <div className="grid grid-cols-2 gap-4">
                        <div className="space-y-2">
                            <Label htmlFor="start">Effective Date</Label>
                            <Input
                                id="start"
                                type="date"
                                required
                                value={formData.effective_date}
                                onChange={(e) => setFormData({ ...formData, effective_date: e.target.value })}
                            />
                        </div>
                        <div className="space-y-2">
                            <Label htmlFor="end">End Date</Label>
                            <Input
                                id="end"
                                type="date"
                                required
                                value={formData.end_date}
                                onChange={(e) => setFormData({ ...formData, end_date: e.target.value })}
                            />
                        </div>
                    </div>

                    {error && <div className="text-red-500 text-sm">{error}</div>}

                    <DialogFooter>
                        <Button type="button" variant="outline" onClick={onClose}>Cancel</Button>
                        <Button type="submit" disabled={loading}>
                            {loading ? "Saving..." : "Save Contract"}
                        </Button>
                    </DialogFooter>
                </form>
            </DialogContent>
        </Dialog>
    );
}
