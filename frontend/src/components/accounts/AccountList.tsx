import { Tier } from "@/types/account";
import type { Account } from "@/types/account";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";

interface AccountListProps {
    accounts: Account[];
}

export function AccountList({ accounts }: AccountListProps) {
    const navigate = useNavigate();

    const getTierColor = (tier?: Tier) => {
        switch (tier) {
            case Tier.ENTERPRISE: return "default"; // violet/black
            case Tier.MID_MARKET: return "secondary"; // gray
            case Tier.SMB: return "outline";
            default: return "outline";
        }
    };

    return (
        <div className="rounded-md border">
            <Table>
                <TableHeader>
                    <TableRow>
                        <TableHead>Name</TableHead>
                        <TableHead>Type</TableHead>
                        <TableHead>Tier</TableHead>
                        <TableHead>Industry</TableHead>
                        <TableHead className="text-right">Actions</TableHead>
                    </TableRow>
                </TableHeader>
                <TableBody>
                    {accounts.map((account) => (
                        <TableRow key={account.id} className="cursor-pointer hover:bg-muted/50" onClick={() => navigate(`/accounts/${account.id}`)}>
                            <TableCell className="font-medium">{account.name}</TableCell>
                            <TableCell>
                                <Badge variant="outline">{account.account_type.replace("_", " ")}</Badge>
                            </TableCell>
                            <TableCell>
                                <Badge variant={getTierColor(account.tier)}>{account.tier}</Badge>
                            </TableCell>
                            <TableCell>{account.industry || "-"}</TableCell>
                            <TableCell className="text-right">
                                <Button variant="ghost" size="sm">View</Button>
                            </TableCell>
                        </TableRow>
                    ))}
                    {accounts.length === 0 && (
                        <TableRow>
                            <TableCell colSpan={5} className="h-24 text-center">
                                No accounts found.
                            </TableCell>
                        </TableRow>
                    )}
                </TableBody>
            </Table>
        </div>
    );
}
