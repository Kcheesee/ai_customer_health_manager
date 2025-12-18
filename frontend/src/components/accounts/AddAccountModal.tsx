import { useState } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger, DialogFooter } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { AccountType, Tier } from "@/types/account";
import type { AccountCreate } from "@/types/account";
import { accountService } from "@/services/accountService";

interface AddAccountModalProps {
    onAccountAdded: () => void;
}

export function AddAccountModal({ onAccountAdded }: AddAccountModalProps) {
    const [open, setOpen] = useState(false);
    const [loading, setLoading] = useState(false);
    const [formData, setFormData] = useState<AccountCreate>({
        name: "",
        account_type: AccountType.STANDARD,
        account_email: "",
        industry: "",
        tier: Tier.MID_MARKET,
        check_in_interval_days: 14
    });

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (!formData.name.trim()) {
            alert("Account name is required");
            return;
        }

        setLoading(true);
        try {
            await accountService.createAccount(formData);
            setOpen(false);
            setFormData({
                name: "",
                account_type: AccountType.STANDARD,
                account_email: "",
                industry: "",
                tier: Tier.MID_MARKET,
                check_in_interval_days: 14
            });
            onAccountAdded();
        } catch (error) {
            console.error("Failed to create account", error);
            alert("Failed to create account. Please try again.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <Dialog open={open} onOpenChange={setOpen}>
            <DialogTrigger asChild>
                <Button>Add Account</Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[425px]">
                <DialogHeader>
                    <DialogTitle>Add New Account</DialogTitle>
                </DialogHeader>
                <form onSubmit={handleSubmit} className="grid gap-4 py-4">
                    <div className="grid gap-2">
                        <Label htmlFor="name">Account Name</Label>
                        <Input
                            id="name"
                            value={formData.name}
                            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                            required
                        />
                    </div>
                    <div className="grid gap-2">
                        <Label htmlFor="type">Type</Label>
                        <Select
                            value={formData.account_type}
                            onValueChange={(val: AccountType) => setFormData({ ...formData, account_type: val })}
                        >
                            <SelectTrigger>
                                <SelectValue placeholder="Select type" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value={AccountType.STANDARD}>Standard</SelectItem>
                                <SelectItem value={AccountType.ELA_PARENT}>ELA Parent</SelectItem>
                                <SelectItem value={AccountType.ELA_CHILD}>ELA Child</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>
                    <div className="grid gap-2">
                        <Label htmlFor="account_email">Contact Email</Label>
                        <Input
                            id="account_email"
                            type="email"
                            placeholder="contact@company.com"
                            value={formData.account_email || ""}
                            onChange={(e) => setFormData({ ...formData, account_email: e.target.value || undefined })}
                        />
                    </div>
                    <div className="grid gap-2">
                        <Label htmlFor="industry">Industry</Label>
                        <Input
                            id="industry"
                            value={formData.industry || ""}
                            onChange={(e) => setFormData({ ...formData, industry: e.target.value })}
                        />
                    </div>
                    <div className="grid gap-2">
                        <Label htmlFor="tier">Tier</Label>
                        <Select
                            value={formData.tier}
                            onValueChange={(val: Tier) => setFormData({ ...formData, tier: val })}
                        >
                            <SelectTrigger>
                                <SelectValue placeholder="Select tier" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectItem value={Tier.ENTERPRISE}>Enterprise</SelectItem>
                                <SelectItem value={Tier.MID_MARKET}>Mid-Market</SelectItem>
                                <SelectItem value={Tier.SMB}>SMB</SelectItem>
                                <SelectItem value={Tier.STARTUP}>Startup</SelectItem>
                            </SelectContent>
                        </Select>
                    </div>
                    <DialogFooter>
                        <Button type="submit" disabled={loading}>
                            {loading ? "Creating..." : "Create Account"}
                        </Button>
                    </DialogFooter>
                </form>
            </DialogContent>
        </Dialog>
    );
}
